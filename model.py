import os
import torch
import pandas as pd
import re

from transformers import AutoModelForSequenceClassification

import torch
from torch.utils.data import Dataset

from typing import Dict
from typing import List
from tqdm import tqdm
from augmentation import text_augmentation

class GBVDataset(Dataset):
    '''
    Creates a dataset for the model, having a dictionary/JSON file as data input 
    '''

    def __init__(self,
                 data: Dict,
                 tokenizer,
                 max_length: int = 512,
                 class_field = "vies",
                 chunk_type = "vies_contexto",
                 data_type=None):
        '''
        max_length can be changed to better fit the model
        
        class_field indicates the label over which we want to perform the classification task
        e.g. "vies" indicates a classification between bias/no-bias, 
        "resultado" indicates a classification between decision outcomes etc.
        
        chunk_type indicates which chunks will be chosen as input text
        domain = vies_contexto, intro, end, random
        the most appropriate type will depend on the chosen target
        e.g. to classify on the label "vies", "vies_contexto" is the chunk type of choice
        '''
        
        self.texts = []
        self.labels = []
        for item in data.values():
            for text in item[chunk_type]:
                self.texts.append(text)
                if(class_field == 'vies'):
                    self.labels.append(1 if item[class_field][0] != '' else 0)
                else:
                    print("Class codes for other attributes have yet to be implemented.")
                    exit() 
                                
        self.data_type = data_type
        self.max_length = max_length
        self.tokenizer = tokenizer        
        
    def __len__(self):
        return len(self.labels)

    def encode(self, texts,tokenizer):
        '''
        Creates text encoding for the model 
        '''

        encodes = [ tokenizer.encode_plus(text= text, 
                                         truncation=True,
                                         padding='max_length',
                                         max_length=self.max_length,
                                         add_special_tokens=True)
                   for text in texts
                 ]

        return [encode['input_ids'] for encode in encodes], \
               [encode['attention_mask'] for encode in encodes], \

    def __getitem__(self, idx):

        labels = self.labels[idx] if type(self.labels[idx]) is list else [self.labels[idx]]
        texts = self.texts[idx] if type(self.texts[idx]) is list else [self.texts[idx]]

        # performs data augmentation if in training
        #if self.data_type == "train":          
        #    texts = text_augmentation(texts, labels) 

        token_ids, attention_mask = self.encode(texts, self.tokenizer)
        return dict(
               input_ids=torch.LongTensor(token_ids).squeeze(),
               attention_mask=torch.LongTensor(attention_mask).squeeze(),
               labels=torch.LongTensor(labels).squeeze()
        )
    

class BertFineTuner(torch.nn.Module):

    def __init__(self, 
                model_name,
                num_classes):
        
        super().__init__()
        
        self.model = AutoModelForSequenceClassification.from_pretrained(
                                                model_name,
                                                num_labels=num_classes,
                                                cache_dir='.')

        print(self.model.config)

        # freezes embeddings
        for param in self.model.bert.embeddings.parameters():
            param.requires_grad = False

        for layer in self.model.bert.encoder.layer[:-5]: # freezes all but last 5 layers -- fine tuning is performed over them
            for param in layer.parameters():
                param.requires_grad = False 

    def forward(self, input_ids, attention_mask, labels=None):
        '''
        Performs a forward pass through the model
        
        Set output_hidden_states=True to return the model embeddings (check https://huggingface.co/docs/transformers/v4.25.1/en/model_doc/bert#transformers.BertForSequenceClassification.forward.output_hidden_states)
        '''
              
        output = self.model.forward(input_ids=input_ids, 
                                    attention_mask=attention_mask,
                                    labels=labels
                                    )
       
        logits = output['logits']

        return logits

    def to (self, device):
        self.device = device
        self = super().to(device)
        return self
    
class BertBaseline(torch.nn.Module):

    def __init__(self, 
                model_name,
                num_classes):
        
        super().__init__()
        
        self.model = AutoModelForSequenceClassification.from_pretrained(
                                                model_name,
                                                num_labels=num_classes,
                                                cache_dir='.')
        
        
         # freezes embeddings
        for param in self.model.bert.embeddings.parameters():
            param.requires_grad = False

        for layer in self.model.bert.encoder.layer: # freezes the whole network -- fine tuning is performed over last layer only (classifier)
            for param in layer.parameters():
                param.requires_grad = False
                
        self.model.classifier.requires_grad = True
        print(self.model.config)
        

    def forward(self, input_ids, attention_mask, labels=None):
        '''
        Performs a forward pass through the model
        
        Set output_hidden_states=True to return the model embeddings (check https://huggingface.co/docs/transformers/v4.25.1/en/model_doc/bert#transformers.BertForSequenceClassification.forward.output_hidden_states)
        '''
              
        output = self.model.forward(input_ids=input_ids, 
                                    attention_mask=attention_mask,
                                    labels=labels
                                    )
       
        logits = output['logits']

        return logits

    def to (self, device):
        self.device = device
        self = super().to(device)
        return self

