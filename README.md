# op_tula_print_bot

Telegramm "proxy"-bot for simply printing from subnets that are not directly accessible.

install CUPS on LINUX server and add printers by folowwing commands
sudo lpadmin -p kyocera -E -v ipp://10.132.116.220/ipp/print -m everywhere (add printer with ipp)
sudo lpadmin -p ricoh -E -v socket://10.132.116.221/ -P ./Ricoh-SP_C261SFNw-Postscript-Ricoh.ppd (add printer with ppd
driver)

Set added printer names into print_service.py class PrinterNamesEnum (line 13)

Don`t forget create config.json in root directory of project
config.json 's structure should be like following:
{
"token": "BOT TOKEN",
"primary_chat_id": 111111, #Telegram chat id in which the bot will check the user’s membership. If the user is not
present in this chat, the bot will refuse to complete tasks
"admins_list": ["triple6_2la"] #usernames list of all who will have administrator rights for bot
}