import pandas as pd
from datetime import datetime
import pytz
import logging

time_zone = pytz.timezone('Asia/Kolkata')
current_time= datetime.now(time_zone)

logging.basicConfig(format='%(asctime)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p' , filename='auto_pendency.logs' , encoding='utf-8' , level=logging.DEBUG )


try:
    df_secondary = pd.read_csv('ykb_secondary_pending_abhi.csv')
except Exception as E:
    logging.warning(f"Error Secondary File not found:  {E}")
try:
    outbond_df = pd.read_csv('ykb_outbound.csv')
except Exception as E:
    logging.warning(f"Error Outbound file not Found: {E}")
try:
    outbond_12 = pd.read_csv("ykb_outbond_pending_greater_than_12.csv")
except Exception as E:
    logging.warning(f"Error Outbound12 File not found {E}")
try:
    df_ppph = pd.read_csv('ykb_pendency_automation_PPPH.csv')
except Exception as E:
    logging.warning(f"Error PPPH File not Found {E}")
try:
    df_bagging = pd.read_csv('ykb_bagging_pending_automation_abhi.csv')
except Exception as E:
    logging.warning(f"Error while reading the Bagging File {E}")
try:
    df = pd.read_csv("Pendency_automation_report_ageing_greater_than_12.csv")
except Exception as E:
    logging.warning(f"Error while reading PPPH12 File {E}")
try:
    outbond_xd = pd.read_csv('ykb_outbond_crossdock_abhi.csv')
except Exception as E:
    logging.warning(f"Error while Reading the Outbond XD file {E}")
try:
    outbond_sl = pd.read_csv('outbond_semi_large_abhi.csv')
except Exception as E:
    logging.warning(f"Error Outbond SL File not found {E}")




try:
    df_secondary_zo = df_secondary[df_secondary['bag_type_ph'] == "ZO"]
    df_secondary_zo['bag_facility_source_name'].fillna("Not Found" , inplace=True)
    df_secondary_zo_ph  = df_secondary_zo[df_secondary_zo['bag_facility_source_name'].str.contains("DEL_PL|Bhiwadi|Bhiwani|Bilaspur")]
    df_secondary_zo_sph = df_secondary_zo[~df_secondary_zo.index.isin(df_secondary_zo_ph.index)]
    df_secondary_zo_ph1 = df_secondary_zo_ph.groupby('bag_facility_source_name').size()
    df_secondary_zo_sph1 = df_secondary_zo_sph.groupby('bag_facility_source_name').size()
    # print(f"Secondary Pending ZO PH: {sum(df_secondary_zo_ph1)}")
    # print(f"Secondary Pending ZO SPH: {sum(df_secondary_zo_sph1)}")
    # print(f"Secondary Total Pending ZO: {sum(df_secondary_zo_ph1) + sum(df_secondary_zo_sph1)} ")
    df_secondary_b5 = df_secondary[df_secondary['bag_type_ph'] == "B5"]
    df_secondary_b5['bag_facility_source_name'].fillna("Not Found" , inplace=True)
    df_secondary_b5_ph = df_secondary_b5[df_secondary_b5['bag_facility_source_name'].str.contains("DEL_PL|BHiwadi|Bhiwani|Bilaspur")]
    df_secondary_b5_sph = df_secondary_b5[~df_secondary_b5.index.isin(df_secondary_b5_ph.index)]
    df_secondary_b5_ph1 = df_secondary_b5_ph.groupby('bag_facility_source_name').size()
    df_secondary_b5_sph1 = df_secondary_b5_sph.groupby('bag_facility_source_name').size()
    # print(f"Secondary Pending B5 PH: {sum(df_secondary_b5_ph1)}")
    # print(f"Secondary Pending B5 SPH: {sum(df_secondary_b5_sph1)}")
    # print(f"Secondary Total Pending B5: {sum(df_secondary_b5_ph1) + sum(df_secondary_b5_sph1)} ")
    logging.debug(": Success Processing Secondary Pendency File")
except Exception as E:
    logging.error(f"Error while Processing Secondary File:  {E}")


# OutBond Pending Automation Part
try:
    outbond_total = outbond_df['tracking_id_merchant'].sum()
    # print(f"Total Outbond:  {outbond_total}")
    outbond_xd_total = outbond_xd['tracking_id_merchant'].sum()
    # print(f"Total Cross-Dock Outbond:  {outbond_xd_total}")
    outbond_sl_total = outbond_sl['tracking_id_merchant'].sum()
    # print(f"Total OutBond Semi-Large: {outbond_sl_total} ")
    logging.debug(": Success Processing OB Files")
except Exception as E:
    logging.error(f"Error while Processing OB Files:  {E}")


try:
    df_ppph_zo = df_ppph[df_ppph['bag_type_ph'] == "ZO"]
    df_ppph_zo_ph  = df_ppph_zo[df_ppph_zo['bag_facility_source_name'].str.contains("DEL_PL|Bilaspur|Bhiwani|Bhiwadi")]
    zo_ph_shipment_count  = df_ppph_zo_ph['tracking_id_ekart'].sum()
    df_ppph_zo_sph = df_ppph_zo[~df_ppph_zo.index.isin(df_ppph_zo_ph.index)]
    zo_sph_shipment_count = df_ppph_zo_sph['tracking_id_ekart'].sum()
    # print(f"ZO PPPH PH: {zo_ph_shipment_count}")
    # print(f"ZO PPPH SPH: {zo_sph_shipment_count}")
    # print(f"Total ZO Pending:  {zo_ph_shipment_count + zo_sph_shipment_count}")
    df_ppph_b5 = df_ppph[df_ppph['bag_type_ph'] == "B5"]
    df_ppph_b5_ph = df_ppph_b5[df_ppph_b5['bag_facility_source_name'].str.contains("DEL_PL|Bilaspur|Bhiwani")]
    b5_ph_shipment_count = df_ppph_b5_ph['tracking_id_ekart'].sum()
    df_ppph_b5_sph = df_ppph_b5[~df_ppph_b5.index.isin(df_ppph_b5_ph.index)]
    b5_sph_shipment_count = df_ppph_b5_sph['tracking_id_ekart'].sum()
    # print(f"B5 PPPH PH: {b5_ph_shipment_count}")
    # print(f"B5 PPPH SPH: {b5_sph_shipment_count}")
    # print(f"Total B5 Pending:  {b5_ph_shipment_count + b5_sph_shipment_count}")
    logging.debug(f": Success PPPH File ")
except Exception as E:
    logging.debug(f": Error while Processing the PPPH Files : {E}")


# Bagging Pending 
try:
    df_bagging_zo = df_bagging[df_bagging['bag_type_ph'] == "ZO"]
    df_bagging_zo['bag_facility_source_name'].fillna("Not Found" , inplace=True)
    df_bagging_zo_ph = df_bagging_zo[df_bagging_zo['bag_facility_source_name'].str.contains("DEL_PL|Bilaspur|Bhiwadi|Bhiwani")]
    df_bagging_zo_sph = df_bagging_zo[~df_bagging_zo.index.isin(df_bagging_zo_ph.index)]
    zo_ph_bagging_count = df_bagging_zo_ph.groupby("bag_facility_source_name").size()
    zo_sph_bagging_count = df_bagging_zo_sph.groupby('bag_facility_source_name').size()
    # print(f"ZO PH Bagging Pending: {sum(zo_ph_bagging_count)}")
    # print(f"ZO SPH Bagging Pending: {sum(zo_sph_bagging_count)} ")
    # print(f"Total ZO Bagging Pending: {sum(zo_ph_bagging_count)  + sum(zo_sph_bagging_count)}")
    df_bagging_b5 = df_bagging[df_bagging['bag_type_ph']== "B5"]
    df_bagging_b5['bag_facility_source_name'].fillna("Not Found" , inplace=True)
    df_bagging_b5_ph = df_bagging_b5[df_bagging_b5['bag_facility_source_name'].str.contains("DEL_PL|Bilaspur|Bhiwadi|Bhiwani")]
    df_bagging_b5_sph = df_bagging_b5[~df_bagging_b5.index.isin(df_bagging_b5_ph.index)]
    b5_ph_bagging_count = df_bagging_b5_ph.groupby("bag_facility_source_name").size()
    b5_sph_bagging_count = df_bagging_b5_sph.groupby("bag_facility_source_name").size()
    # print(f"B5 PH Bagging Pending:  {sum(b5_ph_bagging_count)}")
    # print(f"B5 SPH Bagging Pending:  {sum(b5_sph_bagging_count)}")
    # print(f"Total B5 Bagging Pending:   {sum(b5_ph_bagging_count)  + sum(b5_sph_bagging_count)}")
    logging.warning(": Success while Processing Bagging File")
except Exception as E:
    logging.warning(f": Error while Processing the Bagging File : {E}")

# PPPH Pending greater than 12 hour
try: 
    df_zo = df[df['bag_type_ph'] == "ZO"]
    df_zo
    df_zo_ph = df_zo[df_zo["bag_facility_source_name"].str.contains("DEL_PL|Bilaspur|Bhiwani")]
    df_zo_ph_wise = df_zo_ph.groupby('bag_facility_source_name').size()
    # print(sum(df_zo_ph_wise))
    df_zo_sph = df_zo[~df_zo.index.isin(df_zo_ph.index)]
    df_zo_sph_wise = df_zo_sph.groupby('bag_facility_source_name').size()
    # print(sum(df_zo_sph_wise))
    df_b5 = df[df['bag_type_ph'] == "B5"]
    df_b5
    df_b5_ph = df_b5[df_b5['bag_facility_source_name'].str.contains("DEL_PL|Bilaspur|Bhiwani")]
    df_b5_ph_wise  = df_b5_ph.groupby('bag_facility_source_name').size()
    # print(sum(df_b5_ph_wise))
    df_b5_sph  = df_b5[~df_b5.index.isin(df_b5_ph.index)]
    df_b5_sph_wise = df_b5_sph.groupby('bag_facility_source_name').size()
    # print(sum(df_b5_sph_wise))
    logging.warning(": Success while Processing the PPPH greater than 12 Aging File")
except Exception as E:
    logging.warning(f": Error while Processing the PPPH greater than 12 Aging File:  {E}")


def calculate_and_categorize_time(dataframe, column_name, current_time  , bucket_name):
    df_time_wise = pd.to_datetime(dataframe[column_name])
    df_hour_wise = (current_time - df_time_wise) / pd.Timedelta(hours=1)
    df_hour_wise = df_hour_wise.round().astype(int)
    
    def categorize_time(hour_diff):
        if hour_diff > 48:
            return '> 48 hours'
        elif hour_diff > 24 and hour_diff < 48:
            return '24-48 hours'
        elif hour_diff > 11:
            return '12-24 hours'
        else:
            return '< 12 hours'
    
    dataframe["hour_diff"] = df_hour_wise
    dataframe[bucket_name] = df_hour_wise.apply(categorize_time)
    data = dataframe[bucket_name].value_counts()
    return data


zo_ph_secondary_total = calculate_and_categorize_time(df_secondary_zo_ph , 'fact_updated_at' , current_time , "ZO Secondary Pending PH: ")
print(zo_ph_secondary_total)
zo_sph_secondary_total = calculate_and_categorize_time(df_secondary_zo_sph , 'fact_updated_at' , current_time , "ZO Secondary Pending SPH: ")
print(zo_sph_secondary_total)
print(f"Total ZO Secondary Pending:    {sum(zo_ph_secondary_total) + sum(zo_sph_secondary_total)}")
b5_ph_secondary_total = calculate_and_categorize_time(df_secondary_b5_ph , 'fact_updated_at' , current_time , "B5 Secondary Pending PH: ")
print(b5_ph_secondary_total)
b5_sph_secondary_total = calculate_and_categorize_time(df_secondary_b5_sph , 'fact_updated_at' , current_time , "B5 Secondary Pending SPH: ")
print(b5_sph_secondary_total)
print(f"Total B5 Secondary Pending:  {sum(b5_ph_secondary_total) + sum(b5_sph_secondary_total)} ")

## Outbond Pending Automation Part
outbond_12_pendency = calculate_and_categorize_time(outbond_12 , 'fact_updated_at' , current_time , "Outbond Pendency")
print(f"OutBond Pendency {outbond_12_pendency}")

# Bagging Pending 
zo_ph_bagging_total = calculate_and_categorize_time(df_bagging_zo_ph , 'fact_updated_at' , current_time , "ZO Bagging Pending PH: ")
print(zo_ph_bagging_total)
zo_sph_bagging_total = calculate_and_categorize_time(df_bagging_zo_sph , 'fact_updated_at' , current_time , "ZO Bagging Pending SPH: ")
print(zo_sph_bagging_total)
print(f"Total ZO Secondary Pending:    {sum(zo_ph_bagging_total) + sum(zo_sph_bagging_count)}")
b5_ph_bagging_total = calculate_and_categorize_time(df_bagging_b5_ph , 'fact_updated_at' , current_time , "B5 Bagging Pending PH: ")
print(b5_ph_bagging_total)
b5_sph_bagging_total = calculate_and_categorize_time(df_bagging_b5_sph , 'fact_updated_at' , current_time , "B5 Bagging Pending SPH: ")
print(b5_sph_bagging_total)
print(f"Total B5 Secondary Pending:  {sum(b5_ph_bagging_total) + sum(b5_sph_bagging_total)} ")

## PPHH Pending 
final_zo_ph = calculate_and_categorize_time(df_zo_ph , 'fact_updated_at' , current_time , 'ZO PH')
print(f"{final_zo_ph} & total {sum(final_zo_ph)}" )
final_zo_sph = calculate_and_categorize_time(df_zo_sph , 'fact_updated_at' , current_time , "ZO SPH")
print(f"{final_zo_sph}  && Total:  {sum(final_zo_sph)}")
print(f"ZO Total PH + SPH =   {sum(final_zo_sph) + sum(final_zo_ph)}")
final_b5_ph = calculate_and_categorize_time(df_b5_ph , 'fact_updated_at' , current_time , "B5 PH")
print(f" {final_b5_ph} && Total:  {sum(final_b5_ph)}")
final_b5_sph = calculate_and_categorize_time(df_b5_sph , 'fact_updated_at' , current_time , "B5 SPH")
print(f"{final_b5_sph} && Total {sum(final_b5_sph)}")
print(f"B5 Final PH + SPH =  {sum(final_b5_ph) + sum(final_b5_sph)}")
