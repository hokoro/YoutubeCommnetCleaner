from transformers import AutoTokenizer
import re
import torch


class Model1:
    def __init__(self, AIpath):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(AIpath, map_location=self.device)
        self.model.eval()
        self.model_text = 'beomi/KcELECTRA-base'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_text)
        self.label = ["긍정","부정","악플","무의미"]

    def predict(self, comment):
        if len(re.compile(r"[\u3131-\u3163\uac00-\ud7a3]+").findall(comment)) == 0:
            return self.label[3]  # 무의미 return

        tokenized_sent = self.tokenizer(
            comment,
            return_tensors="pt",
            truncation=True,
            add_special_tokens=True,
            max_length=128
        )

        tokenized_sent.to(self.device)

        with torch.no_grad():
            outputs = self.model(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"]
            )

        logits = outputs[0]
        logits = logits.detach().cpu()
        result = logits.argmax(-1)

        return self.label[result]
