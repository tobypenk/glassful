library(RMySQL)
library(magrittr)
library(dplyr)
library(stringr)

x <- read.csv(
  "/Users/tobypenk/Desktop/glassful/recipe-scraper/training_data/ingredients_with_ids.csv", 
  header = FALSE,
  stringsAsFactors = FALSE
)
names(x) <- c("content","i_id","source")

fracs <- c("","1/8","1/4","1/2","3/4","1/3","2/3"
           #,"½","¼"
)

nums <- c("",1:4,6,12)

x$begins_with_num <- str_detect(x$content,"^[[:digit:]]") * 1

strip_and_expand <- function(content) {
  total <- c()
  content <- str_replace_all(content,"[[:digit:]]+|/","") %>% trimws()
  for (frac in fracs) {
    total <- c(total,paste0(frac," ",content))
  }
  for (num in sample(nums,2)) {
    for (frac in sample(fracs,2)) {
      total <- c(total,paste0(num," ",frac," ",content) %>% trimws())
    }
  }
  total
}



target = nrow(x)
counter = 0
#for (ct in x$content[x$begins_with_num == 1]) {
for (i in 1:nrow(x)) {
  if (x[i,"begins_with_num"] == 0) next
  
  ct = x[i,"content"]
  print(counter/target)
  if (str_detect(ct," g ") | str_detect(ct," ml ")) next
  expansion <- strip_and_expand(ct)
  for (exp in expansion) {
    x <- rbind(x, c(exp,x[i,"i_id"],"raasipe_db"))
  }
  counter = counter + 1
}

x$content <- trimws(x$content)























x2 <- x %>% subset(.,grepl(" oz ",.$content))

grams <- seq(50,1500,50)
x2$begins_with_num <- str_detect(x2$content,"^[[:digit:]]") * 1
x2 <- x2 %>% subset(.,begins_with_num == 1) %>%
  sample_n(.,1000)

strip_and_expand_metric <- function(content) {
  total <- c()
  content <- str_replace(content," oz ","") %>%
    str_replace_all(.,"[[:digit:]]+|/","") %>% trimws()
  for (gram in sample(grams,2)) {
    total <- c(total,paste0(gram," g ",content))
  }
  for (gram in sample(grams,2)) {
    total <- c(total,paste0(gram,"g ",content))
  }
  for (gram in sample(grams,2)) {
    total <- c(total,paste0(gram," ml ",content))
  }
  for (gram in sample(grams,2)) {
    total <- c(total,paste0(gram,"ml ",content))
  }
  
  total
}



target <- nrow(x2)
counter <- 0

#for (ct in x2$content) {
for (i in 1:nrow(x2)) {
  
  print(counter / target)
  ct <- x2[i,"content"]
  expansion <- strip_and_expand_metric(ct)
  for (exp in expansion) {
    x2 <- rbind(x2, c(exp,x2[i,"i_id"],"raasipe_db"))
  }
  counter <- counter + 1
}



x3 <- rbind(x,x2) %>% unique()
x3$begins_with_num <- NULL
print(nrow(x3))
write.csv(x3,"training_data/augmented_classified_ingredients.csv",row.names = FALSE)



