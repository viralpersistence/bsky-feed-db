import time
import secrets
import sqlalchemy

from atproto import models, IdResolver

from server.client import client
from server.config import HANDLE
from server.database import session, DatabaseUser

def main() -> None:

    id_resolver = IdResolver()
    client_did = id_resolver.handle.resolve(HANDLE)

    # create client proxied to Bluesky Chat service
    dm_client = client.with_bsky_chat_proxy()
    # create shortcut to convo methods
    dm = dm_client.chat.bsky.convo

    password_length = 20

    while True:

        convo_list = dm.list_convos()  # use limit and cursor to paginate
        #print(f'Your conversations ({len(convo_list.convos)}):')
        for convo in convo_list.convos:
            #members = ', '.join(member.did for member in convo.members)
            members = [member.did for member in convo.members]
            #print(members)

            print(len(members))
            print(convo.unread_count)

            if len(members) != 2 or convo.unread_count == 0:
                continue

            print('here')
            print(convo.last_message.text.lower().strip())

            if convo.last_message.text.lower().strip() != 'password':
                continue

            #print(convo.unread_count)
            #print(convo.last_message.text)
            
            #members = ', '.join(member.display_name for member in convo.members)
            #print(f'- ID: {convo.id} ({members})')

            user_did = [did for did in members if did != client_did][0]
            user_password = secrets.token_urlsafe(password_length)

            print("ASDFSAFDSFSDFSDF")

            stmt = sqlalchemy.select(DatabaseUser).filter(DatabaseUser.did == user_did)
            rows = session.execute(stmt).fetchone()

            if rows:
                stmt = sqlalchemy.update(DatabaseUser).where(DatabaseUser.did == user_did).values(password=user_password)
                session.execute(stmt)
            else:
                stmt = sqlalchemy.insert(DatabaseUser).values(did=user_did, password=user_password)
                session.execute(stmt)

            dm.send_message(
                models.ChatBskyConvoSendMessage.Data(
                    convo_id=convo.id,
                    message=models.ChatBskyConvoDefs.MessageInput(
                        text=user_password,
                    ),
                )
            )

            dm.update_read({'convo_id': convo.id})

            '''
            if convo.unread_count > 0:
                dm.send_message(
                    models.ChatBskyConvoSendMessage.Data(
                        convo_id=convo.id,
                        message=models.ChatBskyConvoDefs.MessageInput(
                            text='Hello from Python SDK!',
                        ),
                    )
                )

                #convo.unread_count -= 1
                #print(dir(dm))
                dm.update_read({'convo_id': convo.id})
            '''
            
        time.sleep(60)


if __name__ == '__main__':
    main()

    # test: 'did:plc:x4qyokjtdzgl7gmqhsw4ajqj', 'did:plc:eppsmw5nfmdzhfeymtzd3xbe', 'did:plc:r6wxaadynk3m7sqsyn3r3vrf', 'did:plc:r63juenfni5lyahm4prwvhdg'