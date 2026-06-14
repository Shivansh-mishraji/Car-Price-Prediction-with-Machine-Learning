# Car Price Prediction - MLOps & Full Stack Showcase

This document is designed to help you prepare for job interviews where you showcase this project. It details the "Why," "What," and "How" of your decisions, preparing you for deep-dive technical questions.

## 1. Project Overview & Problem Statement

**The Problem:** The used car market is highly volatile and subjective. Determining the fair value of a car is difficult because it depends on several non-linear factors (age, mileage, brand, transmission, etc.). 
**The Solution:** We built an end-to-end Machine Learning pipeline that predicts the selling price of a car based on historical data, and deployed it via a REST API with a modern web interface.

**Key Achievements to Highlight in Interviews:**
- Transitioned from a raw Jupyter Notebook to a production-ready modular Python codebase.
- Implemented an automated ML pipeline using Scikit-Learn `Pipeline` and `ColumnTransformer`.
- Built a RESTful backend using FastAPI for high performance and automatic documentation.
- Designed a modern, responsive "Glassmorphism" frontend to showcase full-stack capabilities.

---

## 2. Machine Learning Pipeline Decisions

### Why Random Forest?
- **Decision:** We chose Random Forest Regressor over Linear Regression or SVM.
- **Why:** Car prices have non-linear relationships with features (e.g., depreciation is steep in the first few years, then flattens out). Random Forest captures these non-linearities and feature interactions automatically without needing extensive manual feature engineering (like polynomial features).
- **Metric:** We achieved an R² score of ~0.96, meaning 96% of the variance in the car price is predictable from the chosen features.

### Feature Engineering & Preprocessing
- **Handling `Car_Name`:** We dropped it. High cardinality categorical variables lead to massive dimensionality if One-Hot Encoded, and without a massive dataset, it leads to overfitting.
- **Age over Year:** We converted `Year` to `Age` (Current Year - Purchase Year). Age is a more generalized continuous variable for models to understand depreciation.
- **Categorical Variables:** Handled using `OneHotEncoder(drop='first')`. Dropping the first category prevents the "dummy variable trap" (multicollinearity).
- **Numerical Variables:** Handled using `StandardScaler` inside the pipeline to normalize ranges, helping the model converge faster.

---

## 3. MLOps & Architecture Decisions

### Why FastAPI?
- **Performance:** Built on Starlette and Pydantic, it is one of the fastest Python frameworks available.
- **Validation:** Pydantic automatically validates the JSON payload coming from the frontend. If a user sends a string instead of a float for `Present_Price`, FastAPI throws a clean 422 error automatically.
- **Documentation:** Automatically generates Swagger UI (`/docs`), making it easy for frontend developers (or interviewers) to test endpoints without writing code.

### Pipeline Persistence (joblib)
- Instead of just saving the trained model, we saved the *entire scikit-learn Pipeline*.
- **Why it matters:** In production, new data needs the exact same transformations (One-Hot Encoding, Scaling) as the training data. Saving the pipeline guarantees that the production environment doesn't have preprocessing mismatches (data leakage or feature misalignment).

---

## 4. Potential Interview Cross-Questions & Answers

**Q: Your dataset is quite small (~300 rows). Isn't Random Forest prone to overfitting on small datasets?**
*Answer:* Yes, it can be. To mitigate this, we could limit the `max_depth` of the trees or increase `min_samples_split`. We also evaluate using Cross-Validation. However, for a proof-of-concept project, Random Forest provided the best baseline R² score compared to Linear Regression which severely underfitted.

**Q: How would you handle a new `Car_Name` or `Fuel_Type` that the model has never seen?**
*Answer:* For `Fuel_Type`, our `OneHotEncoder` uses `handle_unknown='ignore'`. If a new category appears in production, it will set all one-hot columns to 0 rather than crashing the app. For `Car_Name`, we dropped it precisely for this reason—it prevents the model from breaking on unseen models. 

**Q: How would you scale this application?**
*Answer:* Currently, the model is loaded into memory when the FastAPI app starts. 
- For more traffic: I would deploy the FastAPI app using Docker and scale it horizontally using Kubernetes or AWS ECS. 
- For larger models: I would decouple inference using a message queue (like Celery/RabbitMQ) or host the model on a dedicated inference server like Triton or AWS SageMaker.

**Q: Why use Vanilla CSS instead of Tailwind or Bootstrap?**
*Answer:* To demonstrate a deep understanding of core CSS concepts like CSS Variables, Flexbox/Grid, and modern aesthetic trends (Glassmorphism, animations) without relying on abstractions. It shows I can build a design system from scratch.

---

## 5. Next Steps / Future Enhancements (To mention in interviews)
- **CI/CD Pipeline:** Add GitHub Actions to automatically run `pytest` and build a Docker image on push.
- **Data Drift Monitoring:** Implement a tool like Evidently AI to monitor if the distribution of incoming API requests differs from the training data.
- **Model Retraining:** Add a script to periodically pull new market data and retrain the model if accuracy drops below a threshold.
