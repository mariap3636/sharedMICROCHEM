First demo version of bigger database containing all compounds and all reactions from 102 folders of all pollutants. It is builded from scratch with all information from these folders, downloaded by perl/python scripts.

You can visualise it in Browser for SQLite. There are two tables: 
compounds and reaction, each reaction has column input_id and output_id which reffers to id of each compound in compounds table. 