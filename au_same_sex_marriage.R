# Move to working directory
setwd("~/Documents/Project/analytics_practice")

# Load needed libraries
library(tidyverse)
library(readxl)

# Column headings, in this case territories, are separate from the rest of the data in the xls  
#   file, and are going to be imported separately so that they can be cleaned easier.
territories <- 
  read_excel(
    path = "australian_marriage_law_postal_survey_2017_-_participation_final.xls",
    sheet = "Table 2",
    range = "A7:A41", 
    col_names = "territory") %>%
  # Removing null values
  drop_na()
  # Removing footnotes sometimes included after territory
  mutate(territory = gsub("\\([a-z]\\)", "", territory)) %>%

# Importing the rest of the data for males, and adding back in the territories
male_data <- read_excel(
  path = "australian_marriage_law_postal_survey_2017_-_participation_final.xls",
  sheet = "Table 2",
  range = "B6:R41") %>%
drop_na() %>%
mutate(territory = rep(territories$territory, each = 3), gender = "Male") %>%
    filter(!grepl(pattern = "Total", x = "territory")) %>%
gather(key = "age", value = "count", -X__1, -territory, -gender)
# Fix first column name
colnames(male_data)[1] <- "metric"

# Repeating import step for females
female_data <- read_excel(
  path = "australian_marriage_law_postal_survey_2017_-_participation_final.xls",
  sheet = "Table 3",
  range = "B6:R41") %>%
  drop_na() %>%
  mutate(territory = rep(territories$territory, each = 3), gender = "Female") %>%
  filter(!grepl(pattern = "Total", x = "territory")) %>%
  gather(key = "age", value = "count", -X__1, -territory, -gender)
# Fix first column name
colnames(female_data)[1] <- "metric"

# Combined tidied DataFrames and removed uncombined DataFrames
data <- rbind(female_data, male_data)
rm("male_data", "female_data", "territories")

# Export as CSV
write_csv(x  = data, path = "au_marriage_law_postal_survey_2017_tidied.csv")
