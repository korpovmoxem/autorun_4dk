# -*- coding: utf-8 -*-
import clear_calls, ITS, GRM, X_Report
from SendNotification import send_motification
from SendRequestCreateCurrentMonthDealsDataFile import send_request_create_current_month_deals_data_file
from UpdateDailyTaskStatistic import update_daily_task_statistic


def main():
    clear_calls.main()
    ITS.main()
    GRM.main()
    update_daily_task_statistic()
    X_Report.main()
    send_request_create_current_month_deals_data_file()
    send_motification(['311', '1'], 'Автозапуск вечерних процессов завершен')


main()
