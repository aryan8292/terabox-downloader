from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

goBackTxt = "Go back to main menu"

#level0 applicaple to many places (go back to main menu)
goBackBtn = KeyboardButton(text=goBackTxt)
goBackKeyBoard = ReplyKeyboardMarkup(keyboard=[[goBackBtn]], resize_keyboard=True)

#level 1 keyboard buttons for admins
LinkConverterTxt = "Link Converter"

adminBtn1 = KeyboardButton(text=LinkConverterTxt)
adminKeyboard1 = ReplyKeyboardMarkup(keyboard=[[adminBtn1]],resize_keyboard=True,is_persistent=True)


#level2 keybaord btns for admins
teraboxTxt = "TeraBox Converter"
uploadVidTxt = "Generate link from Videos"

adminBtn2 = KeyboardButton(text=teraboxTxt)
adminBtn3 = KeyboardButton(text=uploadVidTxt)
adminBtn4 = KeyboardButton(text=goBackTxt)
adminKeyboard2 = ReplyKeyboardMarkup(keyboard=[[adminBtn2],[adminBtn3],[adminBtn4]],resize_keyboard=True)