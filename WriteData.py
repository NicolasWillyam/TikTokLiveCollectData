
import gspread
sa = gspread.service_account(filename="keys.json")
sh =  sa.open("TikTokLiveTest")

wks = sh.worksheet ("Client Data")


wks.update('A1', 'Client')