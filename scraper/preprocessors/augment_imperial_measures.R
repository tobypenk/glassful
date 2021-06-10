library(RMySQL)
library(magrittr)
library(dplyr)
library(stringr)

x <- read.csv(
  "/Users/tobypenk/Desktop/glassful/recipe-scraper/data_kernel.csv", 
  stringsAsFactors = FALSE
) %>% subset(.,class==2)

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
for (ct in x$content[x$begins_with_num == 1]) {
  print(counter/target)
  if (str_detect(ct," g ") | str_detect(ct," ml ")) next
  expansion <- strip_and_expand(ct)
  for (exp in expansion) {
    x <- rbind(x, c(exp,2,1))
  }
  counter = counter + 1
}

x$content <- trimws(x$content)

#x2 <- read.csv(
#  "/Users/tobypenk/Desktop/coursera/tf/3 - NLP/week 3/newlabels.csv", 
#  stringsAsFactors = FALSE
#)

#x3 <- rbind(x,x2) %>% unique()



write.csv(x,"/Users/tobypenk/Desktop/glassful/recipe-scraper/new_aug_kernel_imperial.csv",row.names = FALSE)





