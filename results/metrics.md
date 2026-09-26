# Results and modeling decisions

## Dataset profile

| Stage | Rows | Columns | Missing values | Stores |
|---|---:|---:|---:|---:|
| Raw daily sales | 336,084 | 9 | 56,459 | — |
| Raw store master | 406 | 10 | 841 | 402 unique IDs after trimming |
| Clean joined dataset | 119,905 | 23 | 0 | 400 |
| Open-store forecasting data | 99,483 | — | 0 | — |

The raw sales source contained 1,125 duplicate store/date pairs. Four store IDs in the master data were duplicated after whitespace normalization.

## Forecasting design

- Target: `Sales`
- Algorithm: XGBoost regression
- Objective: `reg:squarederror`
- Training period: through 2015-05-31
- Test period: after 2015-05-31
- Train/test rows: 92,592 / 6,891
- Model features after encoding: 29
- Excluded from predictors: `Customers`, technical store ID and constant `Open`

### Hyperparameters

| Parameter | Value |
|---|---:|
| Boosting rounds | 100 |
| `eta` | 0.3 |
| `max_depth` | 6 |
| `lambda` | 1 |
| `alpha` | 1 |
| `subsample` | 1 |
| `colsample_bytree` | 1 |

### Held-out results

| Metric | Value |
|---|---:|
| R² | 0.979 |
| Adjusted R² | 0.979 |
| MAE | 921 |
| RMSE | 2,756 |
| MAPE | 13.9% |

## Clustering design

- Unit of analysis: store
- Stores: 399 after removing outlier store 765
- Engineered features: average sales, average customers, sales per customer, sales coefficient of variation, promotion lift
- Scaling: z-score normalization
- Algorithm: k-means
- `k`: 3
- Initialization: random
- Silhouette coefficient: approximately 0.2477

## Limitations

- The retail dataset covers January 2013 through July 2015 and does not represent current commercial conditions.
- The model was evaluated on a single chronological holdout rather than rolling-origin cross-validation.
- Promotion, holiday and competition features do not capture every local business event.
- The clustering silhouette score is modest; two of the three groups overlap substantially.
- Original course data is not redistributed, so reproducing the exact results requires legitimate access to the source files.
