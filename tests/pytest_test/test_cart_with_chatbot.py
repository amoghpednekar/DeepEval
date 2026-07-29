from deepeval.test_case import LLMTestCase, LLMTestCaseParams;
from deepeval.metrics import GEval
from deepeval.evaluate import AsyncConfig, evaluate
from conftest import chat, get_cart, clear_cart
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


class TestCartUpdateCorrectness:

    @pytest.mark.parametrize("item_to_add,item_detail",[
        ("add 2 trail running shoes size UK 9 color black/white to my cart", "trail running shoes"),
        ("add 2 Merino Wool Sweater of size L of colour Oatmeal to my cart", "Merino Wool Sweater"),
        ("add 3 DDR4 RAM Kit of RAM 8GB and 3600MHz speed to my cart", "DDR4 RAM by Corsair")
    ])

    @pytest.mark.parametrize("update_item",[
        "reduce to",
        "lower to",
        "change quantity to ",
        "change quantity of ",
        "update to",
        "make it"
    ])

    def test_update_cart_via_chat(self,judge,session_id,item_to_add,item_detail,update_item):
        #Arrange
        #step 0 - Clear cart before
        #clear cart
        clear_cart(session_id=session_id)

        #Step 1 - Add items to cart
        chat(item_to_add, session_id)

        #Act
        #Step 2 - Update items from cart
        update_prompt=f"{update_item} of {item_detail} to 1"
        chat(update_prompt,session_id)

        cart_details = get_cart(session_id)

        cart_actual_output = json.dumps(cart_details, indent=2)


        update_cart_count_correctness = GEval(
            name = "Update cart count correctness",
            criteria = (
                "evaluate whether the items in the cart is matches {item_detail} as requested by user"
                "verify the quantity in the cart matches the requested count exactly"
            ),
            evaluation_steps=[
                "check the total quantiy of item in the cart is equal to the requested quantity of 1"
            ],
            evaluation_params = [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold = 0.7,
            model = judge
        )

        test_case1 = LLMTestCase(
            input=update_prompt,
            actual_output= cart_actual_output
        )

        evaluate(test_cases =[test_case1],
                metrics = [update_cart_count_correctness],
                async_config=AsyncConfig(run_async=False)
        )
