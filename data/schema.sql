CREATE TABLE "rate_plan" (
	"Rate_Paln_Product_Id"	INTEGER,
	"Rate_Plan_code"	INTEGER,
	"Rate_Plan_Description"	TEXT,
	"Rate_Plan_Type"	TEXT,
	"Rate_Plan_Group"	TEXT,
	PRIMARY KEY("Rate_Paln_Product_Id")
);

CREATE TABLE "network_activity_type" (
	"Network_Activity_Type_Code"	INTEGER,
	"Network_Activity_Type_Name"	TEXT NOT NULL,
	PRIMARY KEY("Network_Activity_Type_Code")
);

CREATE TABLE info_model (
	"Subscription_Id" BIGINT, 
	"Running_Date" DATE, 
	"Rate_Plan_Product_Id" BIGINT, 
	"Call_Gap_Days" BIGINT, 
	"Most_Used_Governorate" TEXT, 
	"Most_Used_Qism" TEXT, 
	"Most_Used_Region" TEXT, 
	"Duality_Flag" TEXT
);

CREATE TABLE agg_revenue_subs_daily (
	"Subscription_Id" BIGINT, 
	"Revenue_Date" DATE, 
	"Total_Revenue" BIGINT, 
	"Recharges" BIGINT, 
	"Baki_Revenue" BIGINT, 
	"Nota_Revenue" BIGINT, 
	"Connect_Revenue" BIGINT, 
	"Admin_Fees" BIGINT, 
	"Tesla_Revenue" BIGINT, 
	"Balance_Transfer_Fees" BIGINT
);

CREATE TABLE agg_network_activity_daily (
	"Subscription_Id" BIGINT, 
	"Rate_Plan_Product_Id" BIGINT, 
	"Network_Activity_Type_Code" BIGINT, 
	"Duration" BIGINT, 
	"Data_Volumne" BIGINT, 
	"Running_Date" DATE
);