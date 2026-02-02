from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# class FormRegister(StatesGroup):
#     currency = State()
#     step_order = State()
#     step_price = State()
#     max_orders = State()
#     exchange = State()
#     select = State()
#     api_key = State()
#     secret_key = State()
# ------------------  PROFILE ---------------------
def get_keyboard_profile_info(is_profile: bool = False, isActive: bool = False) -> InlineKeyboardMarkup:
    if not is_profile:
        profile_info_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📄 Create account",
                                                                                            callback_data="create_account")],
                                                                      [InlineKeyboardButton(text="‹ Back", callback_data="main_menu")]])
    else:
        execute = "🛑 STOP" if isActive else "🟢 START"
        profile_info_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=execute,
                                                                                            callback_data="profile_change_active")],
                                                                      [InlineKeyboardButton(text="⚙️ Settings",
                                                                                            callback_data="profile_change_settings")],
                                                                      [InlineKeyboardButton(text="📊 Statistics",
                                                                                            callback_data="profile_statistics")],
                                                                      [InlineKeyboardButton(text="‹ Back", callback_data="main_menu")]])



    return profile_info_keyboard

return_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="« Menu", callback_data="main_menu")]])

return_profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="‹ Back", callback_data="profile"),
                                                                 InlineKeyboardButton(text="« Menu", callback_data="main_menu")]])
