from unittest.mock import patch

from pytest import raises

from taskmasterexp.ai.errors import MessageTooLongError
from taskmasterexp.ai.messages import _send_split_message

TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer cursus augue quis lorem pretium, non dictum lacus ultricies. Morbi aliquam felis a venenatis imperdiet. Nullam id dapibus eros. Suspendisse eget ipsum iaculis, fringilla tortor et, malesuada arcu. Ut auctor, mauris non blandit fringilla, massa ante mollis metus, ut efficitur nunc elit vel enim. Sed vel fringilla risus, sed finibus quam. Mauris non magna in dui rhoncus consequat id vestibulum augue. In posuere finibus diam nec consectetur. Proin venenatis dictum hendrerit. Fusce accumsan rutrum leo, et venenatis lectus interdum ac. Duis tincidunt imperdiet tellus, id pellentesque ipsum aliquam sit amet. Quisque condimentum augue nec nulla fermentum gravida nec et odio. Pellentesque malesuada neque libero, non vehicula nulla pellentesque at. Aenean ultrices ante a ligula laoreet lacinia. Aenean in tempor massa. Duis gravida nisi vel felis consequat pretium.

Aenean et metus placerat dui consequat scelerisque et id nibh. Ut interdum ante sit amet elit sagittis sollicitudin. Duis in neque vitae odio fringilla elementum eu eget leo. Sed semper eleifend purus, eget mattis massa blandit eu. Suspendisse dapibus felis dignissim tellus ullamcorper, sed accumsan nisi sodales. Sed eget aliquam velit, non auctor nisi. Integer id ornare nisi. Curabitur nisi felis, eleifend porttitor laoreet a, feugiat sed mi. Praesent ligula elit, aliquet nec quam sit amet, lobortis congue dolor. Cras porta massa ac dui auctor, sed ornare enim auctor. Pellentesque at convallis justo, eu faucibus sem. In vulputate imperdiet dolor, vel lacinia dolor faucibus a. Interdum et malesuada fames ac ante ipsum primis in faucibus.

In finibus tellus mi, nec feugiat lacus posuere ut. Curabitur ornare dui erat, vitae suscipit nisi dapibus in. Suspendisse potenti. Nulla euismod eros vel lorem aliquam, eu elementum neque tristique. Ut commodo ipsum eget ipsum pharetra dignissim. In congue metus quis lorem facilisis, a finibus elit tincidunt. Class id.
"""  # noqa: E501


@patch("taskmasterexp.ai.messages._send_message")
async def test_send_split_message(mock_send_message):
    result_text = []

    def _send_message(_, text: str, destination: str):
        result_text.append(text)
        assert len(text) <= 1300
        assert destination == "1234567890"

    mock_send_message.side_effect = _send_message

    assert len(TEXT) > 1300
    assert mock_send_message.call_count == 0

    await _send_split_message(None, TEXT, "1234567890")

    mock_send_message.assert_called()
    assert TEXT == "\n".join(result_text)
    assert mock_send_message.call_count == 2


@patch("taskmasterexp.ai.messages._send_message")
async def test_send_split_message_long_paragraph(mock_send_message):
    text = "a" * 1400
    assert len(text) > 1300

    with raises(MessageTooLongError):
        await _send_split_message(None, text, "1234567890")


def test_webhook(test_client, mock_twilio_client):
    mock_twilio_client.messages.create.assert_not_called()
    response = test_client.post(
        "/messages/webhook",
        content="From=1234567890&Body=Hello&ProfileName=Test&WaId=1234567890",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == 204
    mock_twilio_client.messages.create.assert_called()
