import os, zipfile, json, asyncio, datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
ZIP_PATH = os.getenv("SAMPLE_ZIP", "./scripts/whatsapp sample payloads.zip")

# MongoDB connection
client = AsyncIOMotorClient(MONGO_URI)
db = client.whatsapp
col = db.processed_messages

def normalize_msg(obj):
    """
    Extract a single message from your payload format.
    Handles the 'metaData.entry' nesting in your provided sample.
    """
    try:
        meta = obj.get("metaData", {})
        entries = meta.get("entry", [])
        if not entries:
            return None

        changes = entries[0].get("changes", [])
        if not changes:
            return None

        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        contacts = value.get("contacts", [])

        if not messages:
            return None

        m = messages[0]
        contact_info = contacts[0] if contacts else {}
        profile_name = contact_info.get("profile", {}).get("name")
        wa_id = contact_info.get("wa_id")

        # Convert epoch string to datetime
        ts_str = m.get("timestamp")
        if ts_str:
            ts_dt = datetime.datetime.utcfromtimestamp(int(ts_str))
        else:
            ts_dt = datetime.datetime.utcnow()

        return {
            "msg_id": m.get("id"),
            "meta_msg_id": None,
            "wa_id": wa_id,
            "from": m.get("from"),
            "to": value.get("metadata", {}).get("phone_number_id"),
            "text": m.get("text", {}).get("body"),
            "timestamp": ts_dt,
            "status": "sent",
            "direction": "inbound",
            "name": profile_name
        }

    except Exception as e:
        print("Error normalizing message:", e)
        return None


    # Example: flat "messages" array at root
    if "messages" in obj:
        m = obj["messages"][0]
        return {
            "msg_id": m.get("id"),
            "meta_msg_id": None,
            "wa_id": m.get("from"),
            "from": m.get("from"),
            "to": m.get("to"),
            "text": m.get("text", {}).get("body") if isinstance(m.get("text"), dict) else m.get("text"),
            "timestamp": datetime.datetime.utcnow(),
            "status": "sent",
            "direction": "inbound",
            "name": None
        }
    return None

async def process_json_obj(obj):
    # Status update events
    if obj.get("statuses"):
        for s in obj["statuses"]:
            msgid = s.get("id") or s.get("message_id")
            status = s.get("status")
            if msgid:
                await col.update_one(
                    {"msg_id": msgid},
                    {"$set": {"status": status, "status_updated_at": datetime.datetime.utcnow()}},
                    upsert=False
                )
    else:
        # Normal message events
        m = normalize_msg(obj)
        if m and m.get("msg_id"):
            await col.update_one(
                {"msg_id": m["msg_id"]},
                {"$setOnInsert": m},
                upsert=True
            )

async def process_zip(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        for fname in z.namelist():
            if not fname.lower().endswith(".json"):
                continue
            with z.open(fname) as f:
                try:
                    obj = json.load(f)
                    await process_json_obj(obj)
                except Exception as e:
                    print(f"Error processing {fname}: {e}")

if __name__ == "__main__":
    asyncio.run(process_zip(ZIP_PATH))
    print("✅ Done processing zip:", ZIP_PATH)
