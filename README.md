# S.M.A.R.T. exporter for Prometheus

## 概要

Prometheus で HDD の S.M.A.R.T. 情報を収集するためのスクリプトです．

## 機能

HDD に関する次の属性を出力します．

- #1    Raw_Read_Error_Rate
- #5    Reallocated_Sector_Ct
- #194  Temperature_Celsius
- #196  Reallocated_Event_Count
- #197  Current_Pending_Sector
- #198  Offline_Uncorrectable