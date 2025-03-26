#### Python Script

1. This project processes sample cell count data and generates boxplots to compare immune cell populations. To run, download the project and install the dependencies listed in `requirements.txt` into your local Python environment (i.e. `pip install -r requirements.txt`). Next, run the script (i.e. `python technical_script.py`). The script will process `cell-count.csv`, creating a new file `new_cell_count.csv` in the `data/` folder. Additionally, it will generate boxplots for each of the 5 immune cell populations, saving them in the `figures/` folder.

2. Visually, only two of the resulting boxplots, those for `cd4_t_cell` and `monocyte`, show a notable difference between responders and non-responders. This observation is confirmed by a t-test, which yields p-values below the standard 0.05 threshold for 95% confidence, indicating a statistically significant difference.


#### Database

1. One approach would be to organize the data in a relational database using SQL. A prototype schema is included below...

    ![drawSQL-image-export-2025-03-26](https://github.com/user-attachments/assets/5d421096-d554-4d88-823c-5eab8cb473a4)

2. Relational databases offer several advantages, including scalability, optimization, accessibility, organization, and security. Storing the data this way could thus facilitate additional research, analysis, and collaboration.

3. Query to summarize the number of subjects available for each condition...  
    ```
    SELECT condition, COUNT(patient_id) AS patient_count
    FROM patient
    GROUP BY condition;
    ```

4. Query to return all melanoma PBMC samples at baseline (`time_from_treatment_start` is 0) from patients who have treatment `tr1`...  
    ```
    SELECT s.sample
    FROM sample s
    JOIN patient p USING(patient_id)
    WHERE p.condition = 'Melanoma' AND s.type = 'PBMC' AND s.time_from_start = 0 AND p.treatment = 'tr1';
    ``` 

5.  
    a. Based on previous query, how many samples from each project?  
    ```
    SELECT pr.project_id, COUNT(s.sample) AS sample_count
    FROM sample s
    JOIN project pr USING(project_id)
    JOIN patient p USING(patient_id)
    WHERE p.condition = 'Melanoma' AND s.type = 'PBMC' AND s.time_from_start = 0 AND p.treatment = 'tr1'
    GROUP BY pr.project_id;
    ```

    b. Based on previous query, how many responders/non-responders?  
    ```
    SELECT p.response, COUNT(s.sample) AS sample_count
    FROM sample s
    JOIN patient p USING(patient_id)
    WHERE p.condition = 'Melanoma' AND s.type = 'PBMC' AND s.time_from_start = 0 AND p.treatment = 'tr1'
    GROUP BY p.response;
    ``` 

    c. Based on previous query, how many males/females?  
    ```
    SELECT p.sex, COUNT(s.sample) AS sample_count
    FROM sample s
    JOIN patient p USING(patient_id)
    WHERE p.condition = 'Melanoma' AND s.type = 'PBMC' AND s.time_from_start = 0 AND p.treatment = 'tr1'
    GROUP BY p.sex;
    ```
