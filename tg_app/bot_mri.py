from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import logging
import asyncio
import os
from dotenv import load_dotenv
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
from efficientnet_pytorch import EfficientNet

# Load environment variables
load_dotenv()

TOKEN = os.environ.get('TELEGRAM_TOKEN')
img_size = (224, 224)

if TOKEN is None:
    print("Error: Bot token is not set. Please check your .env file.")
    exit()

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

image_counter = 1

async def process_start_command(message: Message):
    await message.answer(
        '''Привет!\nДанный бот создан для предсказания типа опухоли головного мозга на основе МРТ.\nПожалуйста, загрузи снимок.'''
    )


async def process_help_command(message: Message):
    await message.answer('Загрузи снимок МРТ головного мозга для оценки наличия опухоли.')


async def reply(message: types.Message):
    await message.reply('Пожалуйста, загрузи снимок МРТ')

async def photo(message: types.Message):
    global image_counter
    image_filename = f'brain_MRI_{image_counter}.jpg'
    await message.bot.download(file=message.photo[-1].file_id, destination=image_filename)
    prediction = await one_photo_predict(image_filename, img_size, model)  # Await the coroutine
    await message.answer(prediction)
    os.remove(image_filename)
    image_counter += 1

class CustomEfficientNetB3(nn.Module):
    def __init__(self, num_classes):
        super(CustomEfficientNetB3, self).__init__()
        self.base_model = EfficientNet.from_pretrained('efficientnet-b3')
        self.pooling = nn.AdaptiveMaxPool2d(1)
        self.bn = nn.BatchNorm1d(self.base_model._fc.in_features, momentum=0.99, eps=0.001)
        self.fc1 = nn.Linear(self.base_model._fc.in_features, 256)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.4)
        self.fc2 = nn.Linear(256, num_classes)
        
    def forward(self, x):
        x = self.base_model.extract_features(x)
        x = self.pooling(x).squeeze(-1).squeeze(-1)
        x = self.bn(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

num_classes = 4  
model = CustomEfficientNetB3(num_classes)
model.load_state_dict(torch.load('tg_app/model_pytorch.pth'))


async def one_photo_predict(image_path: str, img_size: tuple, model):

    image = Image.open(image_path).convert('RGB')

    transform = transforms.Compose([
                transforms.Resize(img_size),
                transforms.ToTensor(),
                ])
    
    image = transform(image).unsqueeze(0)  # Add batch dimension

    model.eval()
    with torch.no_grad():
        predictions = model(image)
    
    # Get the class with the highest probability
    predicted_class = torch.argmax(predictions, dim=1)

    class_dict_local = {
        0: 'Предсказанный тип опухоли: Опухоль гипофиза',
        1: 'Опухоль моделью не обнаружена',
        2: 'Предсказанный тип опухоли: Менингиома',
        3: 'Предсказанный тип опухоли: Глиома'
    }
    
    predicted_class_literal = class_dict_local[predicted_class.item()]
    return f'{predicted_class_literal}'

# Register handlers
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(photo, F.photo)
dp.message.register(reply)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

