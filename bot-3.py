@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    butons = ["Ozbek", "Ruscha", "English"]
    keyboard.add(*butons)

    await message.answer(
        text=f"Welcome to our bot, {message.from_user.full_name}. Ro'yxtadan o'tishingiz kerak."
             f"Buning uchun /auth kommandasiga murojaat qiling",
        reply_markup=keyboard
    )

#finite state machine


keyboard = types.ReplyKeyboardMarkup
keyboard.add(keyboard.KeyboardButton(text="Bekor qilish"))

class Auth(StatesGroup):
    name = State()
    surname = State()
    photo = State()

@dp.message_handler(commands=["auth"])
async def auth(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting: ")
    await Auth.name.set()

@dp.message_handler(state=Auth.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text

    if name.isdigit():
        await message.answer("Siz raqam kiritdingiz. Raqam kiritmang")
    else:
        await state.update_data(name=name)
        await message.answer(text="Hammasi yaxshi. Endi familiyangizni kiriting")
        await Auth.surname.set()

@dp.message_handler(state=Auth.surname)
async def get_surname(message: types.Message, state: FSMContext):
    surname = message.text
    if surname.isdigit():
        await message.answer("Siz raqam kiritdingiz. Raqam kiritmang")
    else:
        await state.update_data(surname=surname)
        await message.answer(text="Zo'r! Endi esa rasmingizni yuboring")
        await Auth.photo.set()

@dp.message_handler(content_types=["photo"], state=Auth.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()    #data={"name": name, "surname": surname, }
    await message.answer_photo(photo=photo,
                               caption=f"Ismi: {data.get('name')}\n"
                                    f"Familiya: {data.get('surname')}"

    )
@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="Bekor qilish", ignore_case=True))
async def cnc_btn(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=True)
    await message.answer(text="Bekor qilish")