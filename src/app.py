from atproto import FirehoseSubscribeReposClient, CAR, models, parse_subscribe_repos_message, firehose_models
from ml import SentimentAnalyzer



class MessageProcessor:
    def __init__(self) -> None:
        self.client = FirehoseSubscribeReposClient()
        self.analyzer = SentimentAnalyzer()

    
    def on_message_handler(self, message: firehose_models.MessageFrame) -> None:
        commit = parse_subscribe_repos_message(message)
        if not isinstance(commit, models.ComAtprotoSyncSubscribeRepos.Commit):
            return
        post_text = self._extract_posts(commit)
        if not post_text:
            return
        sentiment = self.analyzer.analyze(post_text)
        print(post_text, sentiment)


    def _extract_posts(self, commit: models.ComAtprotoSyncSubscribeRepos.Commit) -> str | None:
        car = CAR.from_bytes(commit.blocks)
        for op in commit.ops:
            if op.action == "create" and op.path.startswith(models.ids.AppBskyFeedPost):
                if not op.cid:
                    continue

                record_raw_data = car.blocks.get(op.cid)
                if not record_raw_data:
                    continue
                text = record_raw_data["text"]
                return text if text else None

            

if __name__ == "__main__":
    client = MessageProcessor()
    client.client.start(client.on_message_handler)
