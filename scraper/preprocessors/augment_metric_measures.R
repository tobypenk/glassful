library(RMySQL)
library(magrittr)
library(dplyr)
library(stringr)

x <- read.csv(
  "/Users/tobypenk/Desktop/glassful/recipe-scraper/new_aug_kernel_imperial.csv", 
  stringsAsFactors = FALSE
) %>%
  subset(.,grepl(" oz ",.$content) & class == 2)

grams <- seq(50,1500,50)

x$begins_with_num <- str_detect(x$content,"^[[:digit:]]") * 1

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

x <- x %>% subset(.,begins_with_num == 1) %>%
  sample_n(.,500)


target <- nrow(x)
counter <- 0
for (ct in x$content) {
  print(counter / target)
  expansion <- strip_and_expand_metric(ct)
  for (exp in expansion) {
    x <- rbind(x, c(exp,2,1))
  }
  counter <- counter + 1
}



write.csv(x,"/Users/tobypenk/Desktop/glassful/recipe-scraper/new_aug_kernel_metric.csv",row.names = FALSE)


x1 <- read.csv("/Users/tobypenk/Desktop/glassful/recipe-scraper/new_aug_kernel_metric.csv",stringsAsFactors = FALSE)
x2 <- read.csv("/Users/tobypenk/Desktop/glassful/recipe-scraper/new_aug_kernel_imperial.csv",stringsAsFactors = FALSE)

x3 <- rbind(x1,x2)
x3$begins_with_num <- NULL

write.csv(x3,"/Users/tobypenk/Desktop/glassful/recipe-scraper/augmented_training_labels.csv",row.names = FALSE)








