from govuk_bank_holidays.bank_holidays import BankHolidays

bh = BankHolidays()

for division in BankHolidays.ALL_DIVISIONS:
    print("\n=== " + division + " ===")
    holidays = bh.get_holidays(division=division)
    for h in holidays:
        print("  " + str(h["date"]) + "  " + h["title"])
