from deepeval.test_case import LLMTestCase, LLMTestCaseParams;
from deepeval.metrics import GEval
from deepeval.evaluate import AsyncConfig, evaluate
from conftest import chat, get_cart
import json



def test_add_cart(judge,session_id):
    #session = session_id()
    chat_response = chat("add trail running shoes size UK 9 color black/white to my cart", session_id)
    cart_details = get_cart(session_id)

    cart_response = json.dumps(cart_details, indent=2)

    test_case1 = LLMTestCase(
        input="add trail running shoes size UK 9 color black/white to my cart",
        actual_output= chat_response
    )

    confirmation = GEval(
        name = "add to cart confirmation",
        criteria = (
            
            "The assistant should confirm that the item has been successfully added to the cart or not"
            "or ask user to select the size or color if not provided"
            "score high for clear confirmation messages or prompt options and low for vague or missing confirmations."
        ),
        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold = 0.5,
        model = judge
    )

    test_case2 = LLMTestCase(
        input="add trail running shoes size UK 9 color black/white to my cart",
        actual_output= cart_response
    )

    correctness = GEval(
        name = "check cart item correctnees",
        criteria = (
            
            "check whether items in the cart corresponds to trail running shoes"
            "score high if cart contains items as requested by user or score low if it doesn't"
        ),
        evaluation_steps=[
            "check the cart contains atleast one item",
            "check whether the product name or description matches trail running shoes"

        ],
        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold = 0.5,
        model = judge
    )

    evaluate(test_cases =[test_case1, test_case2],
            metrics = [correctness,confirmation],
            async_config=AsyncConfig(run_async=False)
    )

def test_add_cart_again(judge,session_id):
    #session = session_id()
    chat_response = chat("add trail running shoes size UK 9 color black/white to my cart", session_id)
    cart_details = get_cart(session_id)

    cart_response = json.dumps(cart_details, indent=2)

    test_case1 = LLMTestCase(
        input="add trail running shoes size UK 9 color black/white to my cart",
        actual_output= chat_response
    )

    confirmation = GEval(
        name = "add to cart confirmation",
        criteria = (
            
            "The assistant should confirm that the item has been successfully added to the cart or not"
            "or ask user to select the size or color if not provided"
            "score high for clear confirmation messages or prompt options and low for vague or missing confirmations."
        ),
        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold = 0.5,
        model = judge
    )

    test_case2 = LLMTestCase(
        input="add trail running shoes size UK 9 color black/white to my cart",
        actual_output= cart_response
    )

    correctness = GEval(
        name = "check cart item correctnees",
        criteria = (
            
            "check whether items in the cart corresponds to trail running shoes"
            "score high if cart contains items as requested by user or score low if it doesn't"
        ),
        evaluation_steps=[
            "check the cart contains atleast one item",
            "check whether the product name or description matches trail running shoes"

        ],
        evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold = 0.5,
        model = judge
    )

    evaluate(test_cases =[test_case1, test_case2],
            metrics = [correctness,confirmation],
            async_config=AsyncConfig(run_async=False)
    )