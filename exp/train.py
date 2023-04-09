import os
import torch
import pandas as pd
import numpy as np
import seaborn as sn
import re
import argparse
import matplotlib.pyplot as plt
import time 

from model import GBVDataset
from model import BertFineTuner, BertBaseline 
from sklearn.metrics import balanced_accuracy_score

from transformers import AutoTokenizer
from torch.optim import AdamW

import torch
from torch.utils.data import DataLoader

from typing import Dict
from typing import List
from tqdm import tqdm

import json

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from torch.optim.lr_scheduler import CosineAnnealingLR

    
def prepare_datasets(json_path: str): 

    with open(json_path, 'r') as f:
        data = json.load(f)

    train_keys, test_keys = train_test_split(list(data.keys()), test_size=0.1, random_state=42)
    train_keys, val_keys = train_test_split(train_keys, test_size=0.2, random_state=42)

    train_data = {key: data[key] for key in train_keys}
    val_data= {key: data[key] for key in val_keys}
    test_data = {key: data[key] for key in test_keys}
    
    return train_data, val_data, test_data 


def cm(y_true: list, y_pred: list, phase: str):
    '''
    Builds confusion matrix
    '''
    
    # constant for classes
    classes = (0, 1)

    # confusion matrix
    cf_matrix = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(cf_matrix/np.sum(cf_matrix), index = [i for i in classes],
                     columns = [i for i in classes])
    plt.figure(figsize = (12,7))
    ax = sn.heatmap(df_cm, annot=True, fmt='.2%', vmin=0, vmax=1)
    ax.set(xlabel="Predicted", ylabel="True")
    filename = 'cm_' + phase + '.png'
    plt.savefig(filename)
    plt.close()
    
def eval_graph(train: list, val: list, metric: str):
    '''
    Plots train x val graph of loss or accuracy metrics 
    '''
    x = [i for i in range(len(train))] # # of epochs 
    y1 = train
    y2 = val
    
    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    ax.plot(x, y1, label='train_' + metric)  
    ax.plot(x, y2, label='val_' + metric)  
    ax.set_xlabel('Epochs')  
    ax.set_ylabel(metric)  
    ax.set_title(metric + " over epochs")  
    ax.legend()
    
    filename = 'graph_' + metric + '.png'
    plt.savefig(filename)
    plt.close()
    
def run(args):

    train_data, val_data, test_data = prepare_datasets(args.data_path)  
    
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, cache_dir="transformers")
    trainset = GBVDataset(train_data,
                        tokenizer,
                        args.max_seq_length,
                        data_type='train')

    valset = GBVDataset(val_data,
                        tokenizer,
                        args.max_seq_length,
                        data_type='val')

    testset = GBVDataset(test_data, 
                        tokenizer,
                        args.max_seq_length,
                        data_type='test')
    
    trainloader = DataLoader(trainset, batch_size=args.batch_size, shuffle=True)
    valloader = DataLoader(valset, batch_size=args.batch_size, shuffle=False)
    testloader = DataLoader(testset, batch_size=args.batch_size, shuffle=False) 

    model = BertFineTuner(
        model_name=args.model_name,
        num_classes=args.num_classes
    )
    
    #model = BertBaseline(
    #    model_name=args.model_name,
    #    num_classes=args.num_classes
    #)
    
    device = f'cuda:{args.device}' if args.device.isnumeric() else 'cpu'

    model = model.to(device)

    loss_func = torch.nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=args.lr)
    scheduler = CosineAnnealingLR(optimizer, T_max=len(trainset)//args.batch_size*args.n_epochs, eta_min=1e-8, verbose=True)
    
    def train_step(input):
        # Train
        model.train()
        model.zero_grad()

        input_ids = input['input_ids'].to(device)
        attention_mask = input['attention_mask'].to(device)
        labels = input['labels'].to(device)
        labels_one_hot = torch.nn.functional.one_hot(labels, num_classes=args.num_classes).to(device)
        labels_one_hot = labels_one_hot.float()

        # Forward
        y_logits = model(input_ids, attention_mask, labels)

        # Loss
        loss = loss_func(y_logits, labels_one_hot.to(device))

        # Backpropagation
        loss.backward()
        optimizer.step()
       
        # Accuracy
        y_hat = torch.argmax(y_logits, dim=1)
        #accuracy = (y_hat == labels).type(torch.float).mean() # not balanced
        y_hat = y_hat.cpu().numpy()
        labels = labels.cpu().numpy()
        balanced_accuracy = balanced_accuracy_score(labels, y_hat)
    
        return loss.item(), balanced_accuracy, labels, y_hat

    def validation_step(input):
        # Validation
        model.eval()

        input_ids = input['input_ids'].to(device)
        attention_mask = input['attention_mask'].to(device)
        labels = input['labels'].to(device)
        labels_one_hot = torch.nn.functional.one_hot(labels, num_classes=args.num_classes).to(device)
        labels_one_hot = labels_one_hot.float()

        with torch.no_grad():
            y_logits = model(input_ids, attention_mask)
            loss = loss_func(y_logits, labels_one_hot)
    
            # Accuracy
            y_hat = torch.argmax(y_logits, dim=1)
            #accuracy = (y_hat == labels).type(torch.float).mean() # not balanced
            y_hat = y_hat.cpu().numpy()
            labels = labels.cpu().numpy()
            balanced_accuracy = balanced_accuracy_score(labels, y_hat)
                       
        return loss.item(), balanced_accuracy, labels, y_hat
    
    
    def test_step(input):
             
        input_ids = input['input_ids'].to(device)
        attention_mask = input['attention_mask'].to(device)
        labels = input['labels'].to(device)
        labels_one_hot = torch.nn.functional.one_hot(labels, num_classes=args.num_classes).to(device)
        labels_one_hot = labels_one_hot.float()

        # Forward
        y_logits = model(input_ids, attention_mask, labels)

        # Accuracy
        y_hat = torch.argmax(y_logits, dim=1)
        #accuracy = (y_hat == labels).type(torch.float).mean() # not balanced
        y_hat = y_hat.cpu().numpy()
        labels = labels.cpu().numpy()
        if(1 in y_hat): # if bias was detected in any chunk, all chunks from the same case are assigned the same label
            for i in range(len(y_hat)):
                y_hat[i] = 1
        balanced_accuracy = balanced_accuracy_score(labels, y_hat)

        return balanced_accuracy, labels, y_hat    
    
    start_time = time.time()
    
    train_losses = []
    train_bal_accs = []
    val_losses = []
    val_bal_accs = []
    current_loss_train = float("inf") 
    current_loss_val = float("inf")  
    
    for epoch in tqdm(range(args.n_epochs),leave=True):

        # Training
        train_loss = []
        train_bal_acc = []
        y_true_train = []
        y_pred_train = []
        
        for input in tqdm(trainloader, desc=f"Training Epoch {epoch}", leave=False):
            optimizer.zero_grad()
            train_loss_batch, train_bal_acc_batch, y_true_batch, y_pred_batch = train_step(input)
            optimizer.step()
            train_loss.append(train_loss_batch)
            train_bal_acc.append(train_bal_acc_batch)
            y_true_train.append(y_true_batch.tolist())
            y_pred_train.append(y_pred_batch.tolist())
        scheduler.step()
        train_loss_epoch = np.average(train_loss)
        train_losses.append(train_loss_epoch)
        train_bal_acc_epoch = np.average(train_bal_acc)
        train_bal_accs.append(train_bal_acc_epoch)
        print(f"Epoch {epoch} - Train Loss: {train_loss_epoch:.4f} - Train Balanced Accuracy: {train_bal_acc_epoch:.4f}")
        y_true_train = [item for sublist in y_true_train for item in sublist] # flattens lists of y_true 
        y_pred_train = [item for sublist in y_pred_train for item in sublist] # flattens lists of y_pred
        if(train_loss_epoch < current_loss_train): # if we are in a better epoch than before, lets build a confusion matrix
            cm(y_true_train, y_pred_train, 'train')
            current_loss_train = train_loss_epoch
        else:
            y_true_train = []
            y_pred_train = []

        
        # Validation
        valid_loss = []
        valid_bal_acc = []
        y_true_val = []
        y_pred_val = []
        for input in tqdm(valloader, desc=f"Validation Epoch {epoch}", leave=False):
            optimizer.zero_grad()
            valid_loss_batch, valid_bal_acc_batch, y_true_batch, y_pred_batch = validation_step(input)
            optimizer.step()
            valid_loss.append(valid_loss_batch)
            valid_bal_acc.append(valid_bal_acc_batch)
            y_true_val.append(y_true_batch.tolist())
            y_pred_val.append(y_pred_batch.tolist())
        scheduler.step(valid_loss_batch)
        valid_loss_epoch = np.average(valid_loss)
        val_losses.append(valid_loss_epoch)
        valid_bal_acc_epoch = np.average(valid_bal_acc)
        val_bal_accs.append(valid_bal_acc_epoch)
        print(f"Epoch {epoch} - Validation Loss: {valid_loss_epoch:.4f} - Validation Balanced Accuracy: {valid_bal_acc_epoch:.4f}")
        y_true_val = [item for sublist in y_true_val for item in sublist] # flattens lists of y_true 
        y_pred_val = [item for sublist in y_pred_val for item in sublist] # flattens lists of y_pred
        if(valid_loss_epoch < current_loss_val): # if we are in a better epoch than before, lets build a confusion matrix
            cm(y_true_val, y_pred_val, 'val')
            current_loss_val = valid_loss_epoch
        else:
            y_true_val = []
            y_pred_val = []

    
    # Evaluation    
    eval_graph(train_losses, val_losses, 'loss')
    eval_graph(train_bal_accs, val_bal_accs, 'balanced_accuracy')
    
    # dumps model to disk
    torch.save(model.state_dict(), args.model_output_dir)
    end_time = time.time()
    print("Total training time in seconds:", round(end_time-start_time, 4))
    
    # Test
    start_time = time.time()
    # loads model from disk
    # https://pytorch.org/tutorials/beginner/saving_loading_models.html
    #model = BertFineTuner(
    #    model_name=args.model_name,
    #    num_classes=args.num_classes
    #)
    #model.load_state_dict(torch.load(args.model_output_dir))
    #model = model.to(device)
          
    test_bal_acc = []
    y_true_test = []
    y_pred_test = []
    for input in tqdm(testloader):
        bal_acc, y_true, y_pred = test_step(input)
        test_bal_acc.append(bal_acc)
        y_true_test.append(y_true.tolist())
        y_pred_test.append(y_pred.tolist())

    test_bal_acc_final = np.average(test_bal_acc)
    print("Final balanced accuracy for test set: {}".format(test_bal_acc_final))
    end_time = time.time()
    print("Total testing time in seconds:", round(end_time-start_time, 4))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_output_dir", type=str, required=True,
                        help='The output directory to which the model is saved')
    parser.add_argument("--num_classes", type=int, required=True, default=5,
                        help='Number of classes to be used in the model')
    parser.add_argument("--data_path", type=str, required=True, default='dataset',
                        help='Path to json containing all data')
    parser.add_argument("--batch_size", type=int, default=16,
                        help='Batch size for training (default = 16)')
    parser.add_argument("--max_seq_length", type=int, default=512,
                        help='Maximum sequence length (default = 512)')
    parser.add_argument("--model_name", type=str, default="neuralmind/bert-base-portuguese-cased",
                        help='Name of the model to be used (default = "neuralmind/bert-base-portuguese-cased")')
    parser.add_argument("--n_epochs", type=int, default=4,
                        help='Number of epochs to run fine tuning (default = 4)')
    parser.add_argument("--lr", type=float, default=1e-3,
                        help='Learning Rate')
    parser.add_argument("--device", type=str, default='cpu',
                        help='GPU ID to run the model')
    parser.add_argument("--no_cuda", type=bool, default=False,
                        help='If passed True, gpu will not be used (default = False)')
    parser.add_argument("--seed", type=int, default=42,
                        help='Seed for pseudo-random number generation for pytorch, numpy, python.random (default = 42)')

    args = parser.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    
    run(args)