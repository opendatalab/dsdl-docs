import torch
import time
import numpy as np


from torchvision import models, transforms
from PIL import Image
from dsdl.dataset import DSDLDataset


fields_list = ["Image", "Label"]

train_yaml = f"/nvme/share_data/data/MNIST/dsdl/set-train/train.yaml"
val_yaml = f"/nvme/share_data/data/MNIST/dsdl/set-test/test.yaml"

loc_config = dict(
    type="LocalFileReader",
    working_dir=f"/nvme/share_data/data/MNIST/original"
)


ds_train = DSDLDataset(dsdl_yaml=train_yaml, location_config=loc_config, required_fields=fields_list)
ds_val = DSDLDataset(dsdl_yaml=val_yaml, location_config=loc_config, required_fields=fields_list)


T = {
    "Image": transforms.Compose([
        lambda x: x[0].to_image().convert(mode='RGB'),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    "Label": transforms.Compose([
        lambda x: np.array([x[0].index_in_domain() - 1])
    ])
}

ds_train.set_transform(T)
ds_val.set_transform(T)

dl_train = ds_train.to_pytorch(batch_size=100)
dl_val = ds_val.to_pytorch(batch_size=100)

model = models.resnet18(pretrained=False)

class_nums = 1000
model.fc = torch.nn.Linear(model.fc.in_features, class_nums)  

device = torch.device("cuda:0")

model.to(device)

criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.1)

def train_one_epoch(model, optimizer, data_loader, device, image_key = 'Image', label_key = 'Label'):

    model.train()

    running_loss = 0.0
    start_time = time.time()
    total = 0
    correct = 0
    
    for i, data in enumerate(data_loader):
        # get the inputs; data is a dict contains image and label
        inputs = data[image_key]
        labels = torch.squeeze(data[label_key])

        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs.float())
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
    
        running_loss += loss.item()
        if i % 100 == 0 and i > 0:
            batch_time = time.time()
            cost = (batch_time-start_time)
            print('    [%5d] loss: %.3f, time cost: %.2f, accuracy: %.2f %%' %
                  (i, running_loss, cost, accuracy))

            running_loss = 0.0
            total = 0
            correct = 0


num_epochs = 5
for epoch in range(num_epochs):
    print("------------------ Training Epoch {} ------------------".format(epoch+1))
    train_one_epoch(model, optimizer, dl_train, device)


def test_model(model, data_loader, device, image_key = 'Image', label_key = 'Label'):

    model.eval()

    start_time = time.time()
    total = 0
    correct = 0
    with torch.no_grad():
        for i, data in enumerate(data_loader):
            # get the inputs; data is a dict contains image and label
            inputs = data[image_key]
            labels = torch.squeeze(data[label_key])

            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs.float())

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
            
        print('    Testing accuracy: %.2f %%' %(accuracy))


test_model(model, dl_val, device)