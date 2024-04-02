import engine
import pandas as pd

qns = [ #Out of context question
        "Who are you",
        "I miss my wife.", 
        "How to get rich?", 
        "Can you help me to stop smoking?", 
        "You are not answering my question?",
    #URL1
        "What is the growing health concern?",
       'Why does Singapore needs to address for pre-diabetes and reduce the impact of T2DM and CVD',
       'Report the value for IFG and Fasting Plasma glucose', 
       "How to lead to eat less fat",
       "What is the recommended alcohol intake for male?",
       "What is the side effects of metformin for pre-diabetes",
       "Explain the pathway for managing pre-diabetes",
       "What are the ways to implement lifestyle intervention",
       "Is it good to cycle for 180 mintues per weeks",
       "Who is Dr Gilbert Tan",
       #URL2
       "What is the percentage of people have suffered type 2 diabetes mellitus (T2DM)",
       "What are the leading cause of morbidity and mortality for patients with diabetes",
       "Can you explain what is Personalising T2DM medications",
       "How can Pharmacological treatment plays a key role in managing T2DM",
       "List the benefits for Metformin",
       "When was CVOTS is mandated by the USA",
       "Why patient-centered approach are useful to adopt",
       "What will be the impact of poor medication adherence",
       "How frequently does the diabetics patient need to go for regular review?",
       "Who is the expert who chaired for ACE CLINICAL GUIDANCE",
       #URL3
       "What are the key messages for Gestational diabetes mellitus An update on screening, diagnosis, and follow-up",
       "Describe the steps on 24–28 weeks Screen for GDM in all women without diabetes or pre-diabetes",
       "Why is Glycated haemoglobin (HbA1c) should not be used to screen for or diagnose diabetes during pregnancy?",
       "List out the screening test for All women without diabetes or pre-diabetes (including women at increased risk of diabetes who were not diagnosed during their first trimester).",
       "What is the role for Associate Professor Tan Lay Kok from KKH",
       #URL4
       "Who are the healthcare professionals in the images who take care of diabetes care and recovery journey?",
       "Is it common for a person living with diabetes to receive treatment from a healthcare team consisting of different healthcare professionals",
       "What is the difference between General Practitioner and Endocrinologist?",
       "How can dietitian and pharmacist support for patients with diabetes",
       "Provide the link for Services by General Practitioners (Family Medicine Clinics, Primary, Primary Care Network)",
       #URL5
       "What are the different type pf diabetes tablet?",
       "Should i take Repaglinide before or after the meals"
       "What will be the side effects if I drink alcohol with diabetes tablet?",
       "After taking diabetes tablet, should i inform the doctor if i encounter symptoms such as rash, sore throat?",
       "Should i take my diabetes tablet even when I am not feeling well?",
       #URL6
       "Can diabetes affect the feet?",
       "Why early identification and intervention of diabetic foot ulcers is important",
       "How frequently to check for your feet and toes for cuts, sores etc?",
       "Do we have to wash the diabetic feet everyday with mild soap?",
       "Is it encourage to smoke if I am a diabetics patient",
       #URL 7
       "What Is a Diabetic Ulcer?",
       "How to prevent for diaetic ulcer",
       "Is it encourage to cross the leg while sitting for diabetics patient??",
       "What are the usual things that podiatrist will check during the regular foot examination",
       "When was this 'Sole Saviours' first published?",
       # URL 8
       "Why does a diabetic patient need to learn how to inject insulin",
       "What is inslin?",
       "What are the 3 main areas of injection for insulin?",
       "How long action lasts for Rapid-acting - Lispro?",
       "What is the time of start of action for Long-acting Humulin",
       #URL 9
       "What are the routine vaccinations for children and adults living with diabetes?",
       "What should I know about the influenza vaccination?",
       "What should I know about the pneumococcal vaccination?",
       "Is Prevenar 13 (PCV13) is recommended for infants younger than 4 years old as a series of 4 doses, starting at 2 months of age.",
       "What are the things to tell the doctor when discussing for suitable vaccinations for diabetics",
        #URL 10
        "How can diabetes can cause complications for my body?",
        "What kind of situation can consider as pre-diabetes",
        "Why internal fat can cause problems?",
        "List some of the common myths and facts about diabetes",
        "What is the link between carbohydrates abd insulin?",
        #URL 11
        "Which one is more healthier - wholegrains or white rice?",
        "How are carbohydrates converted to glucose?",
        "Is it good to skip my meals before the buffet?",
        "What is the recommeded sodium content?",
        "List out the 4'As of stress management",
        #URL 12
        "What are the common signs and symptoms of Hypoglycaemia?",
        "How do I know if my weight is within the optimal range?",
        "Why is Blood Sugar Monitoring Important?",
        "How can I prepare for travel?",
        "How can I manage my diabetes while abroad?",
        # URL 13
        "Am I experiencing caregiver stress?",
        "How your outpatient bill may be covered",
        "How to be eligble for Pioneer Generation",
        "What are 23 conditions for outpatient treatment that cover under Chronic Disease Management Programme (CDMP)",
        "What are the helpful questions that i can ask when talking about diabetes with my loved ones"
       ]



# Initialize a pandas DataFrame to store query and response data
df_columns = [
    'reader_query', 'info_retrieved_source', 'llm_response',
    'info_score', 'accuracy_score', 'accuracy_reasoning',
    'runtime_in_sec', 'cost_usd', 'query_token', 'info_token',
    'respond_token', 'total_token'
]
df = pd.DataFrame(columns=df_columns)


ans = []

for q in qns: 
    for i in range(5): #number of testing times (Sufficient for the above questions)
        try:         
            df.loc[len(df)] = engine.ask(q) # update to dataframe
            break #Break the loop 
        except: #If any errors occur such as due to openai 
            continue

df.to_csv('result/sample_output.csv',index=False,encoding='utf-8-sig')