library('openxlsx')
library('dplyr')
library('Hmisc')

data <- read.xlsx('regression_data.xlsx')

formula_without_dummy <- U ~ U_0 + LEAK + VLM_transformed + MV_transformed + RET + VLT + COR
columns_without_dummy <- c('U_0', 'LEAK', 'VLM_transformed', 'MV_transformed', 'RET', 'VLT', 'COR')

data1 <- data %>% filter(PRO_OR_CON == 'PRO')
model1 <- lm(formula=formula_without_dummy, data=data1)
model_summary1 <- summary(model1)
model_summary_coef1 = coef(model_summary1)
write.xlsx(model_summary_coef1, 'output_regression_coeffient.xlsx', sheetName='MODEL-1')

independent_var1 <- data1[, columns_without_dummy]
corr1 = cor(independent_var1, method='pearson')
corr_p1 = rcorr(as.matrix(independent_var1), type='pearson')


data2 <- data %>% filter(PRO_OR_CON == 'CON')
model2 <- lm(formula=formula_without_dummy, data=data2)
model_summary2 <- summary(model2)
model_summary_coef2 = coef(model_summary2)
write.xlsx(model_summary_coef2, 'output_regression_coeffient.xlsx', sheetName='MODEL-2')

independent_var2 <- data2[, columns_without_dummy]
corr2 = cor(independent_var2, method='pearson')
corr_p2 = rcorr(as.matrix(independent_var2), type='pearson')

formula_with_dummy <- U ~ U_0 + LEAK + VLM_transformed + MV_transformed + RET + VLT + COR + DEVENT
columns_with_dummy <- c('U_0', 'LEAK', 'VLM_transformed', 'MV_transformed', 'RET', 'VLT', 'COR', 'DEVENT')

model3 <- lm(formula=formula_with_dummy, data=data)
model_summary3 <- summary(model3)
model_summary_coef3 = coef(model_summary3)
write.xlsx(model_summary_coef3, 'output_regression_coeffient.xlsx', sheetName='MODEL-3')

independent_var3 <- data[, columns_with_dummy]
corr3 = cor(independent_var3, method='pearson')
corr_p3 = rcorr(as.matrix(independent_var3), type='pearson')

