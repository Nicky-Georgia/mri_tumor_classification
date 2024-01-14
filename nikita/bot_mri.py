from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import logging
import asyncio
import os
from dotenv import load_dotenv
from typing import BinaryIO, Union
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.models import load_model

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D , MaxPooling2D , Flatten , Activation , Dense , Dropout , BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam , Adamax
from tensorflow.keras import regularizers




load_dotenv()
loaded_model = load_model('my_model.h5')
TOKEN = os.environ.get('TELEGRAM_TOKEN')
img_size = (224 ,244)
image_path = 'brain1.jpeg'

if TOKEN is None:
    print("Error: Bot token is not set. Please check your .env file.")
    exit()

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Bot:
    @staticmethod
    async def download(file: Union[str, 'Downloadable'],
                       destination: Union[BinaryIO, Path, str, None] = None,
                       timeout: int = 30,
                       chunk_size: int = 65536,
                       seek: bool = True) -> Union[BinaryIO, None]:
        # Your implementation here
        # Make sure to adjust the logic according to your needs
        pass


async def process_start_command(message: Message):
    await message.answer(
        '''Привет!\nДанный бот создан для предсказания типа опухоли головного мозга на основе МРТ.\nПожалуйста, загрузи снимок''')


async def process_help_command(message: Message):
    await message.answer('Загрузи снимок МРТ головного мозга для оценки наличия опухоли')


async def reply(message: types.Message):
    await message.reply('Пожалуйста, загрузи снимок МРТ')


async def photo(message: types.Message):
    await message.bot.download(file=message.photo[-1].file_id, destination='brain_MRI.jpg')
    await message.answer(one_photo_predict('brain_MRI.jpg', img_size, loaded_model))


def one_photo_predict(image_path: str, img_size: tuple, loaded_model):
    image = tf.keras.utils.load_img(image_path, target_size=(img_size[0], img_size[1]))
    image = tf.keras.utils.img_to_array(image)
    image = tf.expand_dims(image, axis=0)
    image = tf.keras.applications.efficientnet.preprocess_input(image)
    predictions = loaded_model.predict(image)
    # Get the index of the highest probability class
    predicted_class = tf.math.argmax(predictions, axis=1)
    class_dict_local = {0: 'glioma', 1: 'meningioma', 2: 'notumor', 3: 'pituitary'}
    predicted_class_literal = class_dict_local[predicted_class.numpy()[0]]
    return f'The predicted class is: {predicted_class_literal}'

#async def show_predict():
    #await one_photo_predict(image_path, img_size, loaded_model)

dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(photo, F.photo)
dp.message.register(reply)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

