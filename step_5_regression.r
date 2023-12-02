library("openxlsx")
library("dplyr")

data_winner <- read.xlsx("regression_data_winner.xlsx")
data_loser <- read.xlsx("regression_data_loser.xlsx")

formula_without_dummy <- U ~ U_0 + LEAK + VLM_transformed + MV_transformed +
  RET + VLT + COR

data_winner_for_model1 <- data_winner %>% filter(PRO_OR_CON == "PRO")
data_loser_for_model1 <- data_loser %>% filter(PRO_OR_CON == "PRO")

model1_winner <- lm(formula = formula_without_dummy,
                    data = data_winner_for_model1)
model1_loser <- lm(formula = formula_without_dummy,
                   data = data_loser_for_model1)

model1_winner_summary <- summary(model1_winner)
model1_loser_summary <- summary(model1_loser)

sink("output_regression_model1_winner.txt")
print(model1_winner_summary)
sink()
sink("output_regression_model1_loser.txt")
print(model1_loser_summary)
sink()

data_winner_for_model2 <- data_winner %>% filter(PRO_OR_CON == "CON")
data_loser_for_model2 <- data_loser %>% filter(PRO_OR_CON == "CON")

model2_winner <- lm(formula = formula_without_dummy,
                    data = data_winner_for_model2)
model2_loser <- lm(formula = formula_without_dummy,
                   data = data_loser_for_model2)

model2_winner_summary <- summary(model2_winner)
model2_loser_summary <- summary(model2_loser)

sink("output_regression_model2_winner.txt")
print(model2_winner_summary)
sink()
sink("output_regression_model2_loser.txt")
print(model2_loser_summary)
sink()

formula_with_dummy <- U ~ U_0 + LEAK + VLM_transformed + MV_transformed +
  RET + VLT + COR + DEVENT

model3_winner <- lm(formula = formula_with_dummy, data = data_winner)
model3_loser <- lm(formula = formula_with_dummy, data = data_loser)

model3_winner_summary <- summary(model3_winner)
model3_loser_summary <- summary(model3_loser)

sink("output_regression_model3_winner.txt")
print(model3_winner_summary)
sink()
sink("output_regression_model3_loser.txt")
print(model3_loser_summary)
sink()

columns_with_dummy <- c("U_0", "LEAK", "VLM", "MV", "RET", "VLT", "COR")

data_pro_winner <- data_winner %>% filter(PRO_OR_CON == "PRO")
data_pro_winner <- data_pro_winner[, columns_with_dummy]

sink("output_summary_pro_winner.txt")
print("min:")
print(sapply(data_pro_winner, min))
print("max:")
print(sapply(data_pro_winner, max))
print("mean:")
print(sapply(data_pro_winner, mean))
print("std:")
print(sapply(data_pro_winner, sd))
sink()

data_pro_loser <- data_loser %>% filter(PRO_OR_CON == "PRO")
data_pro_loser <- data_pro_loser[, columns_with_dummy]

sink("output_summary_pro_loser.txt")
print("min:")
print(sapply(data_pro_loser, min))
print("max:")
print(sapply(data_pro_loser, max))
print("mean:")
print(sapply(data_pro_loser, mean))
print("std:")
print(sapply(data_pro_loser, sd))
sink()

data_con_winner <- data_winner %>% filter(PRO_OR_CON == "CON")
data_con_winner <- data_con_winner[, columns_with_dummy]

sink("output_summary_con_winner.txt")
print("min:")
print(sapply(data_con_winner, min))
print("max:")
print(sapply(data_con_winner, max))
print("mean:")
print(sapply(data_con_winner, mean))
print("std:")
print(sapply(data_con_winner, sd))
sink()

data_con_loser <- data_loser %>% filter(PRO_OR_CON == "CON")
data_con_loser <- data_con_loser[, columns_with_dummy]

sink("output_summary_con_loser.txt")
print("min:")
print(sapply(data_con_loser, min))
print("max:")
print(sapply(data_con_loser, max))
print("mean:")
print(sapply(data_con_loser, mean))
print("std:")
print(sapply(data_con_loser, sd))
sink()