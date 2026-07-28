from deepeval.test_case import LLMTestCase, LLMTestCaseParams;
from deepeval.metrics import GEval
from deepeval.evaluate import AsyncConfig, evaluate
from conftest import chat, get_cart
import json
import pytest



class TestCartClearAwareness:
    @pytest.mark.parametrize("clear_phrase",[
        "clear my cart",
        "remove items from my cart",
        "empty my cart"
    ])
    def test_clear_cart_count_via_chat(self,judge,session_id,clear_phrase):
        #Arrange
        #Step 0 - Add items to cart
        chat("add 2 Merino Wool Sweater of size L of colour Oatmeal to my cart", session_id)

        #Act
        #Step 1 - Remove items from cart
        chat(clear_phrase,session_id)
        cart_details = get_cart(session_id)

        cart_actual_output = json.dumps(cart_details, indent=2)


        clear_cart_count_awareness = GEval(
            name = "Clear Cart Count Awareness",
            criteria = (
                "evaluate whether the items in the cart is empty and fully removed as requested by user"
            ),
            evaluation_steps=[
                "check the total quantiy in the cart is zero"
            ],
            evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold = 0.7,
            model = judge
        )

        test_case1 = LLMTestCase(
            input="add 2 Merino Wool Sweater of size L of colour Oatmeal to my cart",
            actual_output= cart_actual_output
        )

        evaluate(test_cases =[test_case1],
                metrics = [clear_cart_count_awareness],
                async_config=AsyncConfig(run_async=False)
        )
