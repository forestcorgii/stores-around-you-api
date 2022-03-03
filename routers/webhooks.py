
from fastapi import APIRouter,Request,Response,Depends
from pydantic import BaseModel
import httpx, os, logging
from dotenv import load_dotenv
load_dotenv()

VERIFY_TOKEN=os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN=os.getenv('PAGE_ACCESS_TOKEN')

logging. basicConfig(level=logging.WARNING)
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


from dependencies import get_token_header
router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
 


# Request Models.
class WebhookRequestData(BaseModel):
    object: str = ""
    entry: list = []

async def callSendAPI(sender_psid:int, response:object):
    request_body = {
        "recipient":{"id":sender_psid},
        "message":response
    }
    r = httpx.post(
        "https://graph.facebook.com/v13.0/me/messages",
        params={"access_token": PAGE_ACCESS_TOKEN},
        headers={"Content-Type": "application/json"},
        json=request_body,
    )

    logger.debug(r.iter_text())
    r.raise_for_status()


async def handle_message(sender_psid:int, received_message:object):
    if "text" in received_message:
        response = {"text":"hatdog"}
    elif "attachments" in received_message:
        attachment_url = received_message["attachments"][0]["payload"]["url"]
        response = {
      "attachment": {
        "type": "template",
        "payload": {
          "template_type": "generic",
          "elements": [{
            "title": "Is this the right picture?",
            "subtitle": "Tap a button to answer.",
            "image_url": attachment_url,
            "buttons": [
              {
                "type": "postback",
                "title": "Yes!",
                "payload": "yes",
              },
              {
                "type": "postback",
                "title": "No!",
                "payload": "no",
              }
            ],
          }]
        }
      }
    }
    callSendAPI(sender_psid,response)
async def handle_postback(sender_psid:int, received_postbacks:object):
    payload = received_postbacks["payload"]
    if payload == "yes":
        response = {"text":"Thanks"}
    elif payload == "no":
        response = {"text":"Thanks Parin..."}
    callSendAPI(sender_psid,response)

 
# Endpoints.
@router.get("/")
async def verify(request: Request):
    """
    On webook verification VERIFY_TOKEN has to match the token at the
    configuration and send back "hub.challenge" as success.
    """
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get(
        "hub.challenge"
    ):
        if (
            not request.query_params.get("hub.verify_token")
            == VERIFY_TOKEN
        ):
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])

    return Response(content="Required arguments haven't passed.", status_code=400)


@router.post("/")
async def webhook(data: WebhookRequestData):
    """
    Messages handler.
    """
    if data.object == "page":
        for entry in data.entry:
            messaging_events = [
                event for event in entry.get("messaging", []) if event.get("message")
            ]
            # for event in messaging_events:
            message_event = messaging_events[0]
            sender_id = messaging_events[0]["sender"]["id"]
            if "message" in message_event:
                await handle_message(page_access_token=PAGE_ACCESS_TOKEN,
                                    recipient_id=sender_id,
                                    message_text=f"echo: {message_event['text']}")
            elif "postback" in message_event:
                await handle_postback(page_access_token=PAGE_ACCESS_TOKEN,
                                    recipient_id=sender_id,
                                    message_text=f"echo: {message_event['text']}")
 
    return Response(content="ok")

