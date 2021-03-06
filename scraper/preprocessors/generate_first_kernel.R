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

steps <- dbSendQuery(conn, paste0(
  "select trim(replace(replace(instructions,'%20',' '),'+',' ')) content from step;"))
data <- fetch(steps,n=20000)
huh <- dbHasCompleted(steps)
dbClearResult(steps)
dbDisconnect(conn)

data$class = 1
data <- as.data.frame(data)
write.csv(data,"/Users/tobypenk/desktop/glassful/recipe-scraper/all_steps.csv",row.names = FALSE)

#generated by api/fetch_all_materials.php
ings <- readLines("/Users/tobypenk/Desktop/ings.txt") %>%
  as.data.frame()
names(ings)[names(ings) == "."] = "content"
ings$step = 0
ings$ingredient = 1

ttl <- rbind(steps,ings)


write.csv(ttl,"Desktop/ings.csv",row.names = FALSE)


