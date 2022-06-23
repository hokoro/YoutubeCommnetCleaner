import torch
from transformers import AutoTokenizer
import re


class Model2:
    def __init__(self, Sad, Angry, Anxiety, Wound, Panic, model1):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = torch.load(model1, map_location=self.device)
        self.model.eval()
        self.sad = torch.load(Sad, map_location=self.device)
        self.sad.eval()
        self.angry = torch.load(Angry, map_location=self.device)
        self.angry.eval()
        self.anxiety = torch.load(Anxiety, map_location=self.device)
        self.anxiety.eval()
        self.wound = torch.load(Wound, map_location=self.device)
        self.wound.eval()
        self.panic = torch.load(Panic, map_location=self.device)
        self.panic.eval()
        self.model_text = 'beomi/KcELECTRA-base'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_text)
        self.label = ["기쁨", "슬픔", "분노", "불안", "상처", "당황", "욕설", "무의미"]

    def predict(self, comment):
        if len(re.compile(r"[\u3131-\u3163\uac00-\ud7a3]+").findall(comment)) == 0:
            return self.label[7]  # 무의미 return

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

        if result == 0:
            return self.label[0]
        if result == 2:
            return self.label[6]

        # negative model
        negative_per = [0, 0, 0, 0, 0, 0, 0, 0]

        # sad model
        with torch.no_grad():
            outputs = self.sad(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"]
            )
            logits = outputs[0]
            logits = logits.detach().cpu()
            negative_per[1] = float(logits[0][1])

        # angry model
        with torch.no_grad():
            outputs = self.angry(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"]
            )
            logits = outputs[0]
            logits = logits.detach().cpu()
            negative_per[2] = float(logits[0][1])

        # anxiety model
        with torch.no_grad():
            outputs = self.anxiety(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"]
            )
            logits = outputs[0]
            logits = logits.detach().cpu()
            negative_per[3] = float(logits[0][1])
        # wound model
        with torch.no_grad():
            outputs = self.wound(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"]
            )
            logits = outputs[0]
            logits = logits.detach().cpu()
            negative_per[4] = float(logits[0][1])
        # panic model
        with torch.no_grad():
            outputs = self.panic(
                input_ids=tokenized_sent["input_ids"],
                attention_mask=tokenized_sent["attention_mask"],
                token_type_ids=tokenized_sent["token_type_ids"]
            )
            logits = outputs[0]
            logits = logits.detach().cpu()
            negative_per[5] = float(logits[0][1])
        print(negative_per)
        result_max = max(negative_per)
        result = negative_per.index(result_max)

        return self.label[result]
