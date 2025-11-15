import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Iterator

from phi.agent import Agent, RunResponse
from phi.model.openai import OpenAIChat
from phi.run.response import RunEvent
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.log import logger
from phi.utils.pprint import pprint_run_response
from phi.utils.string import hash_string_sha256
from phi.utils.web import open_html_file
from phi.workflow import Workflow

games_dir = Path("/content/tmp/games")
games_dir.mkdir(exist_ok=True, parents=True)
game_output_path = games_dir / "pong-game.html"
game_output_path.unlink(missing_ok=True)

# MODELS
class GameOutput(BaseModel):
    reasoning: str = Field(..., description="Explain your reasoning")
    code: str = Field(..., description="The html5 code for the game")
    instructions: str = Field(..., description="Instruction how to play the game")

class QAOutput(BaseModel):
    reasoning: str = Field(..., description="Explain your reasoning")
    correct: bool = Field(False, description="Does the game pass your criteria?")

# WORKFLOW
class GameGenerator(Workflow):
    description: str = "Generator for single-page HTML5 games"

    # Game Developer Agent
    game_developer: Agent = Agent(
        name="Game Developer Agent",
        description="You generate a fully working HTML5 Pong game.",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Create a PONG game based on the user's prompt.",
            "The game must be pure HTML5 + JS + Canvas (single file).",
            "No external scripts, files, images, or libraries.",

            # REALISTIC GAMEPLAY REQUIREMENTS
            "Gameplay MUST be realistic:",
            " - Player paddle uses acceleration, friction, momentum.",
            " - Player movement is smooth, not instant.",
            " - AI movement is predictive with delayed reaction (not robotic).",
            " - Ball uses angle-based bouncing based on paddle hit position.",
            " - Ball gradually increases speed during play.",
            " - Movement and collisions must feel fluid and natural.",

            # ADDED FEATURE: SPEED PICKER
            "Add a Speed Level Picker (Easy / Medium / Hard) below the Reset button.",
            "Speed affects:",
            " - ball initial velocity",
            " - ball acceleration per hit",
            " - max ball speed",
            " - AI reaction speed",

            # STANDARD FEATURES
            "Game must start when SPACE is pressed.",
            "Player uses W/S to move the left paddle.",
            "Right paddle is controlled by realistic AI.",
            "Display a large score at the top and a 'current score' HUD under the canvas.",
            "Reset button must fully reset match scores, paddle positions, ball movement, state, and speed settings.",
            "Game ends at 10 points.",
            "On loss, use alert() and offer restart/exit.",
            "Embed clear instructions on the HTML page.",
            "Canvas must be large (minimum 900px width).",
            "Colors must be user-friendly and readable.",
            "Code must run standalone when opening the HTML file.",
            "Return ONLY the fields defined in GameOutput."
        ],
        response_model=GameOutput,
    )

    # QA Agent
    qa_agent: Agent = Agent(
        name="QA Agent",
        model=OpenAIChat(id="gpt-4o"),
        description="Evaluate HTML5 Pong code for correctness.",
        instructions=[
            "Verify the HTML5 code is valid and runnable.",
            "Verify the UI layout remains IDENTICAL to the previous version:",
            " - same wrapper layout",
            " - same HUD",
            " - same reset button placement",
            " - same instructions section",
            " - same general appearance and structure",
            "Only permitted additions: speed selector + logic updates.",

            # REALISTIC GAMEPLAY VALIDATION
            "Verify paddle movement is realistic (acceleration, friction, momentum).",
            "Verify AI movement is smoothed, predictive, non-instant.",
            "Verify ball physics include angle reflections and speed growth.",
            "Verify movement is fluid (no stiff or instant movement).",

            # FEATURE VALIDATION
            "Verify speed picker (Easy/Medium/Hard) exists and impacts gameplay:",
            " - initial ball speed",
            " - acceleration curve",
            " - AI difficulty",
            "Verify reset button resets ALL state cleanly.",
            "Verify instruction text is on the page.",
            "Verify scoring system is correct and visible.",
            "Verify alert() triggers on loss and restart works.",
            "Verify game is pure HTML5+JS with no external dependencies.",

            "If EVERYTHING meets requirements, return correct=True.",
            "If ANY realism requirement or UI-structure requirement fails, return correct=False."
        ],
        response_model=QAOutput,
    )

    # MAIN RUN METHOD
    def run(self, game_description: str) -> Iterator[RunResponse]:
        logger.info(f"Game description: {game_description}")

        # Developer agent
        game_output = self.game_developer.run(game_description)

        if game_output and game_output.content and isinstance(game_output.content, GameOutput):
            game_code = game_output.content.code
            logger.info("HTML Game Code generated successfully.")
        else:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="Game generation failed (developer agent)."
            )
            return

        # QA agent
        logger.info("Running QA on the generated game...")

        qa_input = {
            "game_description": game_description,
            "game_code": game_code
        }

        qa_output = self.qa_agent.run(json.dumps(qa_input, indent=2))

        if qa_output and qa_output.content and isinstance(qa_output.content, QAOutput):
            logger.info("QA Agent Response:")
            logger.info(qa_output.content)

            if not qa_output.content.correct:
                raise Exception("QA failed for game code; rejected.")

            game_output_path.write_text(game_code)

            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content=game_output.content.instructions
            )
        else:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="Game generation failed (QA agent)."
            )
            return

generator = GameGenerator()
for r in generator.run("Create an enhanced Pong game"):
    print(r)