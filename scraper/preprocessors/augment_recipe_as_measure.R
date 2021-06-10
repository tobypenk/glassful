library(RMySQL)
library(magrittr)
library(dplyr)

user <- "raasipe_admin"
pass <- "u&z1IGvNgUe7"
host <- "107.180.55.15"
port <- 3306
dbname <- "raasipe"

conn <- dbConnect(MySQL(),
                  user=user,
                  password=pass,
                  dbname=dbname,
                  host=host,
                  port=port)
on.exit(dbDisconnect(con))

rs <- dbSendQuery(conn, paste0(
  "select name from recipe where course <> 'beverage';"))
data <- fetch(rs,n=20000)
huh <- dbHasCompleted(rs)
dbClearResult(rs)
dbDisconnect(conn)

data$name <- paste0("1 recipe ",str_replace_all(data$name,"%20"," ") %>% str_replace_all(.,"\\+"," "))
  
  
write.csv(data,"/Users/tobypenk/Desktop/coursera/tf/3 - NLP/recnames.csv",row.names = FALSE)

  
  
  