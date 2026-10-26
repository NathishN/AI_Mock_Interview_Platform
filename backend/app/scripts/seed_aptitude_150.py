"""Seed 150 Placement Aptitude Questions
Covers:
- Section A: Quantitative Aptitude (Q1 - Q60)
  - Percentages (Q1-10)
  - Profit, Loss & Discount (Q11-18)
  - Ratio & Proportion (Q19-24)
  - Averages (Q25-30)
  - Time & Work (Q31-38)
  - Time, Speed & Distance (Q39-48)
  - Simple & Compound Interest (Q49-52)
  - Number System / HCF / LCM (Q53-60)
- Section B: Logical Reasoning (Q61 - Q105)
  - Number Series (Q61-68)
  - Coding-Decoding (Q69-73)
  - Blood Relations (Q74-77)
  - Direction Sense (Q78-82)
  - Syllogisms (Q83-87)
  - Analogy & Odd One Out (Q88-92)
  - Seating Arrangement (Q93-97)
  - Ranking (Q98-101)
  - Clock & Calendar (Q102-105)
- Section C: Verbal Ability (Q106 - Q130)
  - Synonyms, Antonyms, Grammar & Corrections (Q106-120)
  - Sentence Completion (Q121-125)
  - Para Jumbles (Q126-128)
  - Reading Comprehension Strategy (Q129-130)
- Section D: Data Interpretation (Q131 - Q150)
  - Product Sales Table Analysis (Q131-150)
"""

import logging
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.question import Question, question_fingerprint

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed_aptitude_150")

ROLES = ["Software Development Engineer", "Data Analyst", "Python Developer", "Full-Stack Developer", "Business Analyst"]
STAGES = ["Online Assessment", "Technical Screening"]

RAW_QUESTIONS = [
    # -------------------------------------------------------------
    # SECTION A: QUANTITATIVE APTITUDE (Q1 - Q60)
    # -------------------------------------------------------------
    # --- Percentages ---
    {
        "n": 1, "sub": "Percentages", "d": "Beginner",
        "q": "What is 20% of 250?",
        "ans": "Formula: (Percentage / 100) * Number\nCalculation: (20 / 100) * 250 = 0.20 * 250 = 50.\nQuick Mental Trick: 10% of 250 is 25. Therefore, 20% is 25 * 2 = 50.",
        "kp": ["Formula: (P/100) * N", "Mental math: 10% = 25, so 20% = 50"],
        "cm": ["Dividing 250 by 20 instead of multiplying by 0.2"],
        "fu": ["What is 35% of 250?", "What is 15% of 480?"],
        "tags": ["aptitude", "quantitative", "percentages", "speed-math"]
    },
    {
        "n": 2, "sub": "Percentages", "d": "Beginner",
        "q": "A number is increased by 20% and becomes 360. Find the original number.",
        "ans": "Let the original number be X.\nAn increase of 20% means: X * (1 + 0.20) = 360\n1.20 * X = 360\nX = 360 / 1.20 = 300.\nOriginal number = 300.",
        "kp": ["Original number = Increased Value / (1 + Percentage Increase/100)", "Multiplier for 20% increase is 1.20"],
        "cm": ["Subtracting 20% from 360 (360 - 72 = 288), which is incorrect because the 20% was on the original base, not 360"],
        "fu": ["A number increased by 15% becomes 460. Find the original number."],
        "tags": ["aptitude", "quantitative", "percentages", "reverse-percentage"]
    },
    {
        "n": 3, "sub": "Percentages", "d": "Beginner",
        "q": "A number is decreased by 25% and becomes 300. Find the original number.",
        "ans": "Let the original number be X.\nA decrease of 25% means: X * (1 - 0.25) = 300\n0.75 * X = 300\nX = 300 / 0.75 = 300 * (4 / 3) = 400.\nOriginal number = 400.",
        "kp": ["Original number = Decreased Value / (1 - Percentage Decrease/100)", "0.75 is equivalent to 3/4 fraction"],
        "cm": ["Adding 25% of 300 (300 + 75 = 375), which incorrectly uses 300 as the base"],
        "fu": ["A number decreased by 40% becomes 180. Find the original number."],
        "tags": ["aptitude", "quantitative", "percentages", "reverse-percentage"]
    },
    {
        "n": 4, "sub": "Percentages", "d": "Beginner",
        "q": "A person's salary increases from ₹20,000 to ₹24,000. Find the percentage increase.",
        "ans": "Formula: Percentage Increase = (Absolute Increase / Original Salary) * 100\nAbsolute Increase = 24,000 - 20,000 = ₹4,000\nPercentage Increase = (4,000 / 20,000) * 100 = (1 / 5) * 100 = 20%.\nSalary increase = 20%.",
        "kp": ["Formula: (Change / Original Value) * 100", "Always divide by the original value (₹20,000), not the final value"],
        "cm": ["Dividing by the new salary ₹24,000 instead of the original base"],
        "fu": ["If a person's salary decreases from ₹25,000 to ₹20,000, find the percentage decrease."],
        "tags": ["aptitude", "quantitative", "percentages", "salary-increase"]
    },
    {
        "n": 5, "sub": "Percentages", "d": "Beginner",
        "q": "A price increases by 20% and then decreases by 20%. What is the net percentage change?",
        "ans": "Let initial price be 100.\n1) Increases by 20%: 100 -> 120\n2) Decreases by 20%: 20% of 120 = 24. New price = 120 - 24 = 96.\nNet Change = 96 - 100 = -4% (a 4% decrease).\nFormula for +x% followed by -x%: Net change is always a loss of (x^2 / 100)%.\nHere: (20^2 / 100) = 400 / 100 = 4% decrease.",
        "kp": ["Net change is a 4% decrease, NOT 0%", "Rule: Equal percentage increase and decrease (+x% and -x%) results in a net decrease of (x^2 / 100)%"],
        "cm": ["Assuming +20% and -20% cancel out to 0%"],
        "fu": ["What is the net change when a quantity increases by 30% and then decreases by 30%?"],
        "tags": ["aptitude", "quantitative", "percentages", "successive-change", "top-30"]
    },
    {
        "n": 6, "sub": "Percentages", "d": "Beginner",
        "q": "40% of a number is 80. Find the number.",
        "ans": "Let the number be X.\n0.40 * X = 80\nX = 80 / 0.40 = 200.\nOriginal number = 200.",
        "kp": ["Number = Given Value / Percentage Multiplier", "40% = 2/5; X * 2/5 = 80 => X = 80 * 5/2 = 200"],
        "cm": ["Multiplying 80 by 0.40 (32) instead of dividing"],
        "fu": ["60% of a number is 150. What is 80% of that number?"],
        "tags": ["aptitude", "quantitative", "percentages"]
    },
    {
        "n": 7, "sub": "Percentages", "d": "Beginner",
        "q": "A student scores 360 marks out of 500. Find the percentage scored.",
        "ans": "Formula: (Scored Marks / Total Marks) * 100\nPercentage = (360 / 500) * 100 = (360 / 5) = 72%.\nThe student scored 72%.",
        "kp": ["Percentage = (Obtained / Total) * 100", "Quick division: dividing by 500 and multiplying by 100 is dividing by 5"],
        "cm": ["Inverting the fraction (500 / 360)"],
        "fu": ["If the pass mark is 40%, how many minimum marks were required to pass?"],
        "tags": ["aptitude", "quantitative", "percentages"]
    },
    {
        "n": 8, "sub": "Percentages", "d": "Intermediate",
        "q": "A population increases by 10% annually. If the current population is 10,000, find the population after 2 years.",
        "ans": "Compounded growth formula: P_final = P_initial * (1 + r/100)^t\nYear 1: 10,000 * 1.10 = 11,000\nYear 2: 11,000 * 1.10 = 12,100\nCalculation: 10,000 * (1.10)^2 = 10,000 * 1.21 = 12,100.\nPopulation after 2 years = 12,100.",
        "kp": ["Compound population growth uses (1 + r)^t", "1.1^2 = 1.21; 10,000 * 1.21 = 12,100"],
        "cm": ["Calculating simple interest (10% + 10% = 20% -> 12,000), ignoring compounding on the first year's growth"],
        "fu": ["What would the population be after 3 years at 10% annual growth?"],
        "tags": ["aptitude", "quantitative", "percentages", "compound-growth"]
    },
    {
        "n": 9, "sub": "Percentages", "d": "Beginner",
        "q": "If A is 25% more than B, then B is what percentage less than A?",
        "ans": "Assume B = 100.\nThen A = 125.\nDifference = A - B = 25.\nPercentage B is less than A = (Difference / A) * 100\n= (25 / 125) * 100 = (1 / 5) * 100 = 20%.\nB is 20% less than A.",
        "kp": ["Formula: [r / (100 + r)] * 100", "[25 / 125] * 100 = 20%", "Base shifts from B to A"],
        "cm": ["Assuming B is 25% less than A (common placement trap)"],
        "fu": ["If A is 50% more than B, B is what percentage less than A?"],
        "tags": ["aptitude", "quantitative", "percentages", "comparison", "top-30"]
    },
    {
        "n": 10, "sub": "Percentages", "d": "Beginner",
        "q": "A number is increased by 10% and then by 20%. Find the total percentage increase.",
        "ans": "Method 1 (Successive Formula): a + b + (ab / 100)\n= 10 + 20 + (10 * 20 / 100) = 30 + 2 = 32%.\nMethod 2 (Multiplier): 1.10 * 1.20 = 1.32 => 32% increase.\nTotal percentage increase = 32%.",
        "kp": ["Formula: a + b + (ab/100)", "Multiplier: 1.1 * 1.2 = 1.32 (+32%)"],
        "cm": ["Simply adding 10 + 20 = 30% without compounding"],
        "fu": ["What is the total increase after successive increases of 20% and 30%?"],
        "tags": ["aptitude", "quantitative", "percentages", "successive-increase"]
    },

    # --- Profit, Loss & Discount ---
    {
        "n": 11, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "Cost price = ₹500, Selling price = ₹600. Find the profit percentage.",
        "ans": "Profit = SP - CP = 600 - 500 = ₹100\nProfit Percentage = (Profit / CP) * 100 = (100 / 500) * 100 = 20%.\nProfit = 20%.",
        "kp": ["Profit % is ALWAYS calculated on Cost Price (CP), not Selling Price", "Formula: (SP - CP) / CP * 100"],
        "cm": ["Dividing by SP ₹600 instead of CP ₹500"],
        "fu": ["What would the profit percentage be if SP was ₹750?"],
        "tags": ["aptitude", "quantitative", "profit-loss"]
    },
    {
        "n": 12, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "Cost price = ₹800, Loss = 10%. Find the Selling price.",
        "ans": "Loss Amount = 10% of 800 = ₹80\nSP = CP - Loss = 800 - 80 = ₹720.\nDirect formula: SP = CP * (1 - Loss%/100) = 800 * 0.90 = ₹720.",
        "kp": ["SP = CP * 0.90 for a 10% loss", "Selling Price = ₹720"],
        "cm": ["Adding 10% instead of subtracting"],
        "fu": ["What would be the SP if the loss was 15% on ₹800?"],
        "tags": ["aptitude", "quantitative", "profit-loss"]
    },
    {
        "n": 13, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "Selling price = ₹1,200 with a 20% profit. Find the Cost price.",
        "ans": "SP = CP * (1 + Profit%/100)\n1,200 = CP * 1.20\nCP = 1,200 / 1.20 = ₹1,000.\nCost price = ₹1,000.",
        "kp": ["CP = SP / (1 + Profit%/100)", "Do not compute 20% of 1,200 (that would be profit on SP, not CP)"],
        "cm": ["Subtracting 20% of 1,200 (1,200 - 240 = 960), which is incorrect"],
        "fu": ["If SP is ₹1,350 with 12.5% profit, find CP."],
        "tags": ["aptitude", "quantitative", "profit-loss", "top-30"]
    },
    {
        "n": 14, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "An article marked at ₹1,000 is sold at a 20% discount. Find the selling price.",
        "ans": "Discount Amount = 20% of Marked Price (MP) = 0.20 * 1,000 = ₹200\nSelling Price = MP - Discount = 1,000 - 200 = ₹800.\nDirect: SP = 1,000 * 0.80 = ₹800.",
        "kp": ["Discount is always calculated on Marked Price (MP)", "SP = MP * (1 - Discount%/100)"],
        "cm": ["Confusing Marked Price with Cost Price"],
        "fu": ["If marked price is ₹2,500 and discount is 15%, find SP."],
        "tags": ["aptitude", "quantitative", "discount"]
    },
    {
        "n": 15, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "Successive discounts of 10% and 20% are given on an article. Find the equivalent single discount.",
        "ans": "Let Marked Price = 100.\n1) After 10% discount: 100 -> 90\n2) After 20% discount on 90: 90 - (0.20 * 90) = 90 - 18 = 72.\nEquivalent Single Discount = 100 - 72 = 28%.\nFormula: Single Discount = d1 + d2 - (d1 * d2 / 100) = 10 + 20 - (200 / 100) = 30 - 2 = 28%.",
        "kp": ["Formula: d1 + d2 - (d1 * d2 / 100)", "Equivalent discount is 28%, NOT 30%"],
        "cm": ["Simply adding 10% + 20% = 30%"],
        "fu": ["Find single equivalent discount for successive discounts of 20% and 25%."],
        "tags": ["aptitude", "quantitative", "discount", "successive-discount", "top-30"]
    },
    {
        "n": 16, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "A shopkeeper buys an item for ₹400 and sells it for ₹500. Find the profit percentage.",
        "ans": "Profit = 500 - 400 = ₹100\nProfit % = (100 / 400) * 100 = 25%.\nProfit = 25%.",
        "kp": ["Profit % = (100 / 400) * 100 = 25%"],
        "cm": ["Dividing by 500 resulting in 20%"],
        "fu": ["What if the selling price was ₹480?"],
        "tags": ["aptitude", "quantitative", "profit-loss"]
    },
    {
        "n": 17, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "An article is sold for ₹900 at a 10% loss. Find its Cost price.",
        "ans": "SP = CP * 0.90\n900 = CP * 0.90\nCP = 900 / 0.90 = ₹1,000.\nCost price = ₹1,000.",
        "kp": ["CP = SP / (1 - Loss%/100) = 900 / 0.90 = 1,000"],
        "cm": ["Adding 10% of 900 (990) instead of dividing"],
        "fu": ["If sold for ₹800 at 20% loss, find CP."],
        "tags": ["aptitude", "quantitative", "profit-loss"]
    },
    {
        "n": 18, "sub": "Profit, Loss & Discount", "d": "Beginner",
        "q": "An item costs ₹600. At what price should it be sold to achieve a 25% profit?",
        "ans": "SP = CP * (1 + 0.25) = 600 * 1.25 = ₹750.\nAlternatively: Profit = 25% of 600 = 150. SP = 600 + 150 = ₹750.\nSelling price = ₹750.",
        "kp": ["SP = CP * 1.25 = ₹750"],
        "cm": ["Calculation error on 25% of 600"],
        "fu": ["At what price should it be sold for a 33.33% profit?"],
        "tags": ["aptitude", "quantitative", "profit-loss"]
    },

    # --- Ratio & Proportion ---
    {
        "n": 19, "sub": "Ratio & Proportion", "d": "Beginner",
        "q": "Divide ₹600 in the ratio 2:3.",
        "ans": "Total parts = 2 + 3 = 5 parts.\nValue of 1 part = 600 / 5 = ₹120.\nFirst share = 2 * 120 = ₹240.\nSecond share = 3 * 120 = ₹360.\nShares are ₹240 and ₹360.",
        "kp": ["Sum ratio parts (2 + 3 = 5)", "Each share = (part / total_parts) * total_amount"],
        "cm": ["Dividing by 2 or 3 directly instead of sum of parts"],
        "fu": ["Divide ₹1,200 in the ratio 1:2:3."],
        "tags": ["aptitude", "quantitative", "ratio-proportion"]
    },
    {
        "n": 20, "sub": "Ratio & Proportion", "d": "Beginner",
        "q": "The ratio of boys to girls in a class is 3:2. If the total number of students is 50, find the number of boys.",
        "ans": "Total parts = 3 + 2 = 5 parts.\nNumber of boys = (3 / 5) * 50 = 3 * 10 = 30 boys.\n(Number of girls = 2 * 10 = 20 girls).",
        "kp": ["Boys = (3/5) * 50 = 30"],
        "cm": ["Misidentifying the boys' portion in the ratio (using 2/5 instead of 3/5)"],
        "fu": ["If 5 new girls join, what is the new ratio of boys to girls?"],
        "tags": ["aptitude", "quantitative", "ratio-proportion"]
    },
    {
        "n": 21, "sub": "Ratio & Proportion", "d": "Intermediate",
        "q": "If A:B = 2:3 and B:C = 4:5, find the compound ratio A:B:C.",
        "ans": "Equalize the common term B (LCM of 3 and 4 is 12):\nMultiply A:B by 4: (2 * 4) : (3 * 4) = 8 : 12\nMultiply B:C by 3: (4 * 3) : (5 * 3) = 12 : 15\nCombine: A:B:C = 8 : 12 : 15.",
        "kp": ["Equalize B by multiplying both ratios to match LCM(3, 4) = 12", "Result: 8:12:15"],
        "cm": ["Directly writing 2:3:5 without equalizing B"],
        "fu": ["If A:B = 1:2, B:C = 3:4, and C:D = 5:6, find A:B:C:D."],
        "tags": ["aptitude", "quantitative", "ratio-proportion", "compound-ratio", "top-30"]
    },
    {
        "n": 22, "sub": "Ratio & Proportion", "d": "Beginner",
        "q": "If 5 pens cost ₹100, what is the cost of 8 pens?",
        "ans": "Unitary Method:\nCost of 1 pen = 100 / 5 = ₹20.\nCost of 8 pens = 8 * 20 = ₹160.",
        "kp": ["Unit price = 100 / 5 = ₹20", "Total = 8 * 20 = ₹160"],
        "cm": ["Arithmetic multiplication error"],
        "fu": ["How many pens can be bought with ₹300?"],
        "tags": ["aptitude", "quantitative", "unitary-method"]
    },
    {
        "n": 23, "sub": "Ratio & Proportion", "d": "Beginner",
        "q": "Two numbers are in the ratio 3:5 and their sum is 64. Find the numbers.",
        "ans": "Let the numbers be 3x and 5x.\n3x + 5x = 64\n8x = 64 => x = 8.\nFirst number = 3 * 8 = 24.\nSecond number = 5 * 8 = 40.\nThe numbers are 24 and 40.",
        "kp": ["8x = 64 => x = 8", "Numbers: 24 and 40"],
        "cm": ["Adding 3 + 5 and subtracting from 64"],
        "fu": ["Find the difference between the two numbers."],
        "tags": ["aptitude", "quantitative", "ratio-proportion"]
    },
    {
        "n": 24, "sub": "Ratio & Proportion", "d": "Beginner",
        "q": "If A:B = 4:5 and A = 32, find the value of B.",
        "ans": "A / B = 4 / 5\n32 / B = 4 / 5\n4 * B = 32 * 5 = 160\nB = 160 / 4 = 40.\nAlternatively: 1 part = 32 / 4 = 8; B = 5 * 8 = 40.",
        "kp": ["Cross-multiplication: 4B = 32 * 5 => B = 40"],
        "cm": ["Multiplying 32 by 4/5 instead of 5/4"],
        "fu": ["If B = 60, what would A be?"],
        "tags": ["aptitude", "quantitative", "ratio-proportion"]
    },

    # --- Averages ---
    {
        "n": 25, "sub": "Averages", "d": "Beginner",
        "q": "Find the average of 10, 20, 30, 40, and 50.",
        "ans": "Sum = 10 + 20 + 30 + 40 + 50 = 150.\nCount = 5.\nAverage = Sum / Count = 150 / 5 = 30.\nShortcut: For an arithmetic progression with an odd number of terms, the average is the exact middle term = 30.",
        "kp": ["Average = Sum / Count", "For consecutive AP, Average = Middle term"],
        "cm": ["Miscounting total elements"],
        "fu": ["What is the average of the first 20 even natural numbers?"],
        "tags": ["aptitude", "quantitative", "averages"]
    },
    {
        "n": 26, "sub": "Averages", "d": "Beginner",
        "q": "The average of 5 numbers is 20. Find their total sum.",
        "ans": "Formula: Sum = Average * Count\nSum = 20 * 5 = 100.",
        "kp": ["Sum = Average * Count = 100"],
        "cm": ["Dividing 20 by 5"],
        "fu": ["If a 6th number 26 is added, what is the new average?"],
        "tags": ["aptitude", "quantitative", "averages"]
    },
    {
        "n": 27, "sub": "Averages", "d": "Beginner",
        "q": "The average age of 4 people is 25. A fifth person aged 30 joins. What is the new average age?",
        "ans": "Total age of 4 people = 4 * 25 = 100 years.\nNew total after 5th person joins = 100 + 30 = 130 years.\nNew average = 130 / 5 = 26 years.\nShortcut: The 5th person brings (30 - 25) = 5 extra years. Distribute 5 extra years across 5 people = +1. New average = 25 + 1 = 26.",
        "kp": ["New average = (Old sum + New value) / New count", "Deviation method: extra 5 years / 5 people = +1"],
        "cm": ["Dividing 130 by 4 instead of 5"],
        "fu": ["If the fifth person was aged 20, what would the new average be?"],
        "tags": ["aptitude", "quantitative", "averages", "deviation-method", "top-30"]
    },
    {
        "n": 28, "sub": "Averages", "d": "Beginner",
        "q": "The average of 6 numbers is 15. If one number with value 20 is removed, find the new average.",
        "ans": "Initial Total = 6 * 15 = 90.\nNew Total after removing 20 = 90 - 20 = 70.\nRemaining numbers = 5.\nNew Average = 70 / 5 = 14.",
        "kp": ["New Average = (90 - 20) / 5 = 70 / 5 = 14"],
        "cm": ["Dividing 70 by 6 instead of 5"],
        "fu": ["What if a number with value 10 was removed?"],
        "tags": ["aptitude", "quantitative", "averages"]
    },
    {
        "n": 29, "sub": "Averages", "d": "Beginner",
        "q": "The average of 8 numbers is 25. If each number is increased by 5, what is the new average?",
        "ans": "Property of Averages: If every number in a dataset is increased by a constant k, the average also increases by exactly k.\nNew Average = 25 + 5 = 30.",
        "kp": ["If each item increases by k, average increases by k", "No need to compute individual numbers"],
        "cm": ["Attempting to calculate individual values"],
        "fu": ["What happens if each number is multiplied by 2?"],
        "tags": ["aptitude", "quantitative", "averages", "properties"]
    },
    {
        "n": 30, "sub": "Averages", "d": "Intermediate",
        "q": "Average marks of 10 students is 60. One student with 80 marks leaves. What is the new average?",
        "ans": "Total marks = 10 * 60 = 600.\nRemaining marks after student leaves = 600 - 80 = 520.\nRemaining students = 9.\nNew average = 520 / 9 = 57.78 marks.",
        "kp": ["New Average = (600 - 80) / 9 = 520 / 9 = 57.78"],
        "cm": ["Dividing by 10 instead of 9 remaining students"],
        "fu": ["If the leaving student had 40 marks, how would the average change?"],
        "tags": ["aptitude", "quantitative", "averages"]
    },

    # --- Time & Work ---
    {
        "n": 31, "sub": "Time & Work", "d": "Beginner",
        "q": "A can complete a piece of work in 10 days. What fraction of the work does A complete in one day?",
        "ans": "Work Rate Rule: If a person completes total work in N days, 1 day's work = 1 / N.\nTherefore, in 1 day A completes 1/10 of the work.",
        "kp": ["One day work = 1 / Total days = 1/10"],
        "cm": ["Saying 10 units instead of 1/10th fraction"],
        "fu": ["What fraction of work is done in 4 days?"],
        "tags": ["aptitude", "quantitative", "time-and-work"]
    },
    {
        "n": 32, "sub": "Time & Work", "d": "Beginner",
        "q": "A completes a work in 10 days and B in 15 days. How many days will they take working together?",
        "ans": "Method 1 (Work Rate): A's rate = 1/10, B's rate = 1/15.\nCombined rate = 1/10 + 1/15 = (3 + 2) / 30 = 5/30 = 1/6.\nTime taken = 6 days.\nMethod 2 (LCM Work Units): Total work = LCM(10, 15) = 30 units.\nA's efficiency = 3 units/day; B's efficiency = 2 units/day.\nTogether = 3 + 2 = 5 units/day.\nDays = 30 / 5 = 6 days.\nShortcut Formula: (A * B) / (A + B) = (10 * 15) / 25 = 150 / 25 = 6 days.",
        "kp": ["Formula: (A * B) / (A + B)", "LCM method: 30 units / 5 units per day = 6 days"],
        "cm": ["Averaging the days: (10 + 15)/2 = 12.5 (completely wrong)"],
        "fu": ["How long would they take if C joins who can do it in 30 days?"],
        "tags": ["aptitude", "quantitative", "time-and-work", "top-30"]
    },
    {
        "n": 33, "sub": "Time & Work", "d": "Beginner",
        "q": "A takes 12 days and B takes 18 days to complete a work. How long do they take together?",
        "ans": "Formula: (A * B) / (A + B) = (12 * 18) / (12 + 18) = 216 / 30 = 7.2 days (or 7 1/5 days).\nLCM method: LCM(12, 18) = 36 units. A = 3 u/d, B = 2 u/d. Total = 5 u/d. Time = 36 / 5 = 7.2 days.",
        "kp": ["Formula: (12 * 18) / 30 = 7.2 days", "36 / 5 = 7.2 days"],
        "cm": ["Leaving answer as fraction without simplifying"],
        "fu": ["Convert 7.2 days into days and hours (7 days and 4.8 hours)."],
        "tags": ["aptitude", "quantitative", "time-and-work"]
    },
    {
        "n": 34, "sub": "Time & Work", "d": "Intermediate",
        "q": "A and B together complete a work in 8 days. A alone takes 12 days. How long does B take alone?",
        "ans": "Combined rate (A + B) = 1/8.\nA's rate = 1/12.\nB's rate = 1/8 - 1/12 = (3 - 2) / 24 = 1/24.\nTherefore, B takes 24 days alone.\nFormula: (A * Together) / (A - Together) = (12 * 8) / (12 - 8) = 96 / 4 = 24 days.",
        "kp": ["1/B = 1/Total - 1/A = 1/8 - 1/12 = 1/24", "B alone takes 24 days"],
        "cm": ["Adding rates instead of subtracting"],
        "fu": ["If A and B worked together for 4 days and then A left, how many more days does B need?"],
        "tags": ["aptitude", "quantitative", "time-and-work", "top-30"]
    },
    {
        "n": 35, "sub": "Time & Work", "d": "Beginner",
        "q": "10 workers complete a job in 15 days. How many workers are needed to complete the job in 5 days?",
        "ans": "M1 * D1 = M2 * D2 (Man-days remain constant)\n10 * 15 = M2 * 5\n150 = 5 * M2\nM2 = 150 / 5 = 30 workers.\n30 workers are needed.",
        "kp": ["M1 * D1 = M2 * D2 = Total Man-Days", "10 * 15 = 150 man-days; 150 / 5 = 30 workers"],
        "cm": ["Using direct proportion instead of inverse proportion"],
        "fu": ["How many extra workers must be hired?"],
        "tags": ["aptitude", "quantitative", "man-days"]
    },
    {
        "n": 36, "sub": "Time & Work", "d": "Beginner",
        "q": "A can do a job in 20 days. B is twice as efficient as A. How long does B take alone?",
        "ans": "Efficiency is inversely proportional to time taken.\nIf B is twice as efficient as A, B takes half the time of A.\nTime for B = 20 / 2 = 10 days.",
        "kp": ["Efficiency ratio A:B = 1:2 => Time ratio A:B = 2:1", "Time for B = 20 / 2 = 10 days"],
        "cm": ["Multiplying by 2 instead of dividing (saying 40 days)"],
        "fu": ["How long would they take working together?"],
        "tags": ["aptitude", "quantitative", "efficiency"]
    },
    {
        "n": 37, "sub": "Time & Work", "d": "Beginner",
        "q": "A works for 5 days and completes 1/3 of the work. How many total days are needed to finish the entire job?",
        "ans": "If 1/3 of the work takes 5 days, the total work (1 whole) takes:\nTotal Days = 5 * 3 = 15 days.",
        "kp": ["Total days = Days / Fraction = 5 / (1/3) = 15 days"],
        "cm": ["Dividing 5 by 3"],
        "fu": ["How many more days are needed to finish the remaining work?"],
        "tags": ["aptitude", "quantitative", "time-and-work"]
    },
    {
        "n": 38, "sub": "Time & Work", "d": "Beginner",
        "q": "6 men complete a work in 12 days. How long will 9 men take to complete the same work?",
        "ans": "Formula: M1 * D1 = M2 * D2\n6 * 12 = 9 * D2\n72 = 9 * D2\nD2 = 72 / 9 = 8 days.\n9 men take 8 days.",
        "kp": ["M1 * D1 = M2 * D2", "6 * 12 / 9 = 8 days"],
        "cm": ["Direct proportion error"],
        "fu": ["If 4 men left after 3 days, calculate remaining time."],
        "tags": ["aptitude", "quantitative", "man-days"]
    },

    # --- Time, Speed & Distance ---
    {
        "n": 39, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "A car travels at 60 km/h for 3 hours. Find the distance covered.",
        "ans": "Formula: Distance = Speed * Time\nDistance = 60 km/h * 3 h = 180 km.",
        "kp": ["Distance = Speed * Time = 180 km"],
        "cm": ["Units mismatch"],
        "fu": ["How long would it take to cover this distance at 90 km/h?"],
        "tags": ["aptitude", "quantitative", "speed-distance"]
    },
    {
        "n": 40, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "Distance = 240 km, Speed = 60 km/h. Find the time taken.",
        "ans": "Formula: Time = Distance / Speed\nTime = 240 / 60 = 4 hours.",
        "kp": ["Time = Distance / Speed = 4 hours"],
        "cm": ["Multiplying distance by speed"],
        "fu": ["If speed was 80 km/h, what is the time saved?"],
        "tags": ["aptitude", "quantitative", "speed-distance"]
    },
    {
        "n": 41, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "Convert 72 km/h into meters per second (m/s).",
        "ans": "Conversion factor: Multiply km/h by (5 / 18) to get m/s.\n72 * (5 / 18) = 4 * 5 = 20 m/s.\n72 km/h = 20 m/s.",
        "kp": ["km/h to m/s: Multiply by 5/18", "72 * 5/18 = 20 m/s"],
        "cm": ["Multiplying by 18/5 instead of 5/18"],
        "fu": ["Convert 108 km/h into m/s."],
        "tags": ["aptitude", "quantitative", "speed-conversion", "top-30"]
    },
    {
        "n": 42, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "Convert 20 m/s into km/h.",
        "ans": "Conversion factor: Multiply m/s by (18 / 5) to get km/h.\n20 * (18 / 5) = 4 * 18 = 72 km/h.\n20 m/s = 72 km/h.",
        "kp": ["m/s to km/h: Multiply by 18/5", "20 * 18/5 = 72 km/h"],
        "cm": ["Inverting conversion factor"],
        "fu": ["Convert 25 m/s into km/h."],
        "tags": ["aptitude", "quantitative", "speed-conversion"]
    },
    {
        "n": 43, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "A train travels 300 km in 5 hours. What is its average speed?",
        "ans": "Average Speed = Total Distance / Total Time\nAverage Speed = 300 / 5 = 60 km/h.",
        "kp": ["Average speed = Total distance / Total time = 60 km/h"],
        "cm": ["Arithmetic error"],
        "fu": ["What is this speed in m/s (16.67 m/s)?"],
        "tags": ["aptitude", "quantitative", "speed-distance"]
    },
    {
        "n": 44, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "Two people travel at 40 km/h and 60 km/h in the same direction. What is their relative speed?",
        "ans": "Relative Speed (Same Direction) = Speed1 - Speed2\nRelative Speed = 60 - 40 = 20 km/h.",
        "kp": ["Same direction: Subtract speeds (S1 - S2 = 20 km/h)", "Opposite direction: Add speeds"],
        "cm": ["Adding speeds when moving in the same direction"],
        "fu": ["How much lead will the faster person have after 2 hours?"],
        "tags": ["aptitude", "quantitative", "relative-speed", "top-30"]
    },
    {
        "n": 45, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "Two trains travel in opposite directions at 50 km/h and 70 km/h. What is their relative speed?",
        "ans": "Relative Speed (Opposite Directions) = Speed1 + Speed2\nRelative Speed = 50 + 70 = 120 km/h.",
        "kp": ["Opposite directions: Add speeds (S1 + S2 = 120 km/h)"],
        "cm": ["Subtracting speeds"],
        "fu": ["Convert relative speed 120 km/h into m/s (33.33 m/s)."],
        "tags": ["aptitude", "quantitative", "relative-speed"]
    },
    {
        "n": 46, "sub": "Time, Speed & Distance", "d": "Beginner",
        "q": "A man walks at 5 km/h. How long does he take to cover 15 km?",
        "ans": "Time = Distance / Speed = 15 / 5 = 3 hours.",
        "kp": ["Time = 15 / 5 = 3 hours"],
        "cm": ["Dividing speed by distance"],
        "fu": ["If he runs at 10 km/h, how much time is saved?"],
        "tags": ["aptitude", "quantitative", "speed-distance"]
    },
    {
        "n": 47, "sub": "Time, Speed & Distance", "d": "Intermediate",
        "q": "A train 100 meters long travels at 20 m/s. How much time does it take to cross a telephone pole?",
        "ans": "When crossing a point object (pole, person), distance = length of train.\nDistance = 100 meters.\nSpeed = 20 m/s.\nTime = Distance / Speed = 100 / 20 = 5 seconds.",
        "kp": ["Crossing a pole: Distance = Train length", "Time = 100 / 20 = 5 seconds"],
        "cm": ["Assuming pole has length"],
        "fu": ["How long to cross a platform of length 200m (total distance 300m = 15 seconds)?"],
        "tags": ["aptitude", "quantitative", "trains", "top-30"]
    },
    {
        "n": 48, "sub": "Time, Speed & Distance", "d": "Intermediate",
        "q": "If speed increases by 25%, by what percentage does time decrease for the same distance?",
        "ans": "Distance is constant, so Speed and Time are inversely proportional: S1 * T1 = S2 * T2.\nNew Speed = 1.25 * S1 = (5/4) * S1.\nNew Time = T1 / (5/4) = (4/5) * T1 = 0.80 * T1 = 80% of original time.\nPercentage decrease in time = 100% - 80% = 20% decrease.\nFormula: [x / (100 + x)] * 100 = [25 / 125] * 100 = 20%.",
        "kp": ["Speed increases by 1/4 => Time decreases by 1/(4+1) = 1/5 = 20%", "Product constancy rule"],
        "cm": ["Assuming time decreases by 25%"],
        "fu": ["If speed increases by 50%, by what percentage does time decrease (33.33%)?"],
        "tags": ["aptitude", "quantitative", "speed-time-relationship", "top-30"]
    },

    # --- Simple & Compound Interest ---
    {
        "n": 49, "sub": "Simple & Compound Interest", "d": "Beginner",
        "q": "Find the Simple Interest (SI) on ₹5,000 at 10% per annum for 2 years.",
        "ans": "Formula: SI = (P * R * T) / 100\nSI = (5,000 * 10 * 2) / 100 = 100,000 / 100 = ₹1,000.\nSimple Interest = ₹1,000.",
        "kp": ["SI = (P * R * T) / 100 = ₹1,000", "SI is identical every year (₹500/yr)"],
        "cm": ["Compounding interest instead of simple"],
        "fu": ["What is the total amount payable?"],
        "tags": ["aptitude", "quantitative", "simple-interest"]
    },
    {
        "n": 50, "sub": "Simple & Compound Interest", "d": "Beginner",
        "q": "Find the total Amount under Simple Interest for ₹5,000 at 10% for 2 years.",
        "ans": "Amount = Principal + Simple Interest\nPrincipal = ₹5,000\nSI = (5,000 * 10 * 2) / 100 = ₹1,000\nAmount = 5,000 + 1,000 = ₹6,000.",
        "kp": ["Amount = P + SI = 5000 + 1000 = ₹6,000"],
        "cm": ["Confusing SI with Amount"],
        "fu": ["What would be the amount after 3 years?"],
        "tags": ["aptitude", "quantitative", "simple-interest"]
    },
    {
        "n": 51, "sub": "Simple & Compound Interest", "d": "Intermediate",
        "q": "Find the Compound Interest (CI) on ₹10,000 at 10% per annum for 2 years compounded annually.",
        "ans": "Formula: Amount = P * (1 + R/100)^T\nAmount = 10,000 * (1.10)^2 = 10,000 * 1.21 = ₹12,100.\nCompound Interest = Amount - Principal = 12,100 - 10,000 = ₹2,100.\nShortcut: Year 1 interest = 1,000. Year 2 interest = 1,000 + (10% of 1,000) = 1,100. Total = ₹2,100.",
        "kp": ["A = P * (1 + r)^t = 10,000 * 1.21 = 12,100", "CI = A - P = ₹2,100"],
        "cm": ["Calculating simple interest (₹2,000) instead of compound interest"],
        "fu": ["What is CI for 3 years at 10% (₹3,310)?"],
        "tags": ["aptitude", "quantitative", "compound-interest", "top-30"]
    },
    {
        "n": 52, "sub": "Simple & Compound Interest", "d": "Intermediate",
        "q": "Find the difference between Compound Interest and Simple Interest on ₹10,000 at 10% for 2 years.",
        "ans": "Method 1: CI = ₹2,100; SI = (10,000 * 10 * 2)/100 = ₹2,000.\nDifference = 2,100 - 2,000 = ₹100.\nMethod 2 (2-Year Shortcut Formula): Difference = P * (R / 100)^2\nDifference = 10,000 * (10 / 100)^2 = 10,000 * (1/10)^2 = 10,000 * (1/100) = ₹100.",
        "kp": ["Formula for 2 years: Diff = P * (R/100)^2", "Difference = 10,000 * (0.01) = ₹100"],
        "cm": ["Using the 2-year formula for a 3-year problem"],
        "fu": ["What is the 3-year formula: P*(R/100)^2 * (3 + R/100)?"],
        "tags": ["aptitude", "quantitative", "ci-si-difference", "top-30"]
    },

    # --- Number System / HCF / LCM ---
    {
        "n": 53, "sub": "Number System", "d": "Beginner",
        "q": "Find the HCF (Highest Common Factor) of 24 and 36.",
        "ans": "Prime Factorization:\n24 = 2^3 * 3^1\n36 = 2^2 * 3^2\nHCF = Product of lowest powers of common prime factors = 2^2 * 3^1 = 4 * 3 = 12.\nHCF = 12.",
        "kp": ["HCF takes lowest powers of common primes: 2^2 * 3^1 = 12", "12 divides both 24 and 36 evenly"],
        "cm": ["Confusing HCF with LCM"],
        "fu": ["Find HCF of 48, 72, and 120."],
        "tags": ["aptitude", "quantitative", "hcf-lcm"]
    },
    {
        "n": 54, "sub": "Number System", "d": "Beginner",
        "q": "Find the LCM (Least Common Multiple) of 12 and 18.",
        "ans": "Prime Factorization:\n12 = 2^2 * 3^1\n18 = 2^1 * 3^2\nLCM = Product of highest powers of all prime factors = 2^2 * 3^2 = 4 * 9 = 36.\nLCM = 36.",
        "kp": ["LCM takes highest powers: 2^2 * 3^2 = 36", "Formula: Product = HCF * LCM => 12 * 18 = 6 * 36 = 216"],
        "cm": ["Picking lowest powers instead of highest"],
        "fu": ["Find LCM of 15, 20, and 30."],
        "tags": ["aptitude", "quantitative", "hcf-lcm"]
    },
    {
        "n": 55, "sub": "Number System", "d": "Beginner",
        "q": "Find the smallest number divisible by 6, 8, and 12.",
        "ans": "The smallest number divisible by a set of numbers is their LCM.\n6 = 2 * 3\n8 = 2^3\n12 = 2^2 * 3\nLCM = 2^3 * 3 = 8 * 3 = 24.\nSmallest number = 24.",
        "kp": ["Smallest common multiple = LCM(6, 8, 12) = 24"],
        "cm": ["Multiplying all three numbers together (6*8*12 = 576 is not the smallest)"],
        "fu": ["Find the smallest 3-digit number divisible by 6, 8, and 12 (120)."],
        "tags": ["aptitude", "quantitative", "lcm"]
    },
    {
        "n": 56, "sub": "Number System", "d": "Beginner",
        "q": "What is the remainder when 17 is divided by 5?",
        "ans": "Division Algorithm: Dividend = Divisor * Quotient + Remainder\n17 = 5 * 3 + 2\nRemainder = 2.",
        "kp": ["17 % 5 = 2", "0 <= Remainder < Divisor"],
        "cm": ["Giving quotient (3) instead of remainder (2)"],
        "fu": ["What is the remainder when (-17) is divided by 5 in modular arithmetic (3)?"],
        "tags": ["aptitude", "quantitative", "remainders"]
    },
    {
        "n": 57, "sub": "Number System", "d": "Beginner",
        "q": "Is 97 a prime number? Explain how to check.",
        "ans": "To check if N is prime, test divisibility by prime numbers up to sqrt(N).\nsqrt(97) ≈ 9.84. Prime numbers <= 9 are: 2, 3, 5, 7.\n- 97 is not divisible by 2 (odd)\n- 97 is not divisible by 3 (sum of digits 9+7=16 not div by 3)\n- 97 is not divisible by 5 (does not end in 0 or 5)\n- 97 is not divisible by 7 (97 = 7 * 13 + 6)\nSince 97 is not divisible by any prime <= sqrt(97), 97 is a PRIME number.\nAnswer: Yes.",
        "kp": ["Check divisibility only up to sqrt(N) ≈ 9.84", "Test primes: 2, 3, 5, 7", "97 is prime"],
        "cm": ["Testing all numbers up to 97"],
        "fu": ["Is 91 a prime number? (No, 7 * 13 = 91)."],
        "tags": ["aptitude", "quantitative", "prime-numbers"]
    },
    {
        "n": 58, "sub": "Number System", "d": "Beginner",
        "q": "Find the sum of the first 10 natural numbers.",
        "ans": "Formula: Sum = n * (n + 1) / 2\nFor n = 10:\nSum = 10 * (11) / 2 = 5 * 11 = 55.",
        "kp": ["Sum = n(n + 1) / 2", "10 * 11 / 2 = 55"],
        "cm": ["Adding manually and making an arithmetic slip"],
        "fu": ["Find the sum of the first 50 natural numbers (1,275)."],
        "tags": ["aptitude", "quantitative", "number-series"]
    },
    {
        "n": 59, "sub": "Number System", "d": "Beginner",
        "q": "Find the sum of the first 10 odd natural numbers.",
        "ans": "Formula: Sum of first n odd natural numbers = n^2\nFor n = 10:\nSum = 10^2 = 100.\n(1 + 3 + 5 + 7 + 9 + 11 + 13 + 15 + 17 + 19 = 100).",
        "kp": ["Sum of first n odd numbers = n^2", "10^2 = 100"],
        "cm": ["Using n(n+1)/2 formula instead of n^2"],
        "fu": ["What is the sum of the first 25 odd numbers (625)?"],
        "tags": ["aptitude", "quantitative", "number-series"]
    },
    {
        "n": 60, "sub": "Number System", "d": "Intermediate",
        "q": "What is the greatest number that divides 355, 54, and 103 leaving the same remainder in each case?",
        "ans": "When a number divides A, B, and C leaving the same remainder, the required number is the HCF of the absolute differences between the numbers:\nDifferences:\n|355 - 103| = 252\n|355 - 54| = 301\n|103 - 54| = 49\nFind HCF(252, 301, 49):\nFactors of 49 = 1, 7, 49.\nCheck 49: 252 / 49 = not divisible.\nCheck 7:\n252 / 7 = 36 (divisible)\n301 / 7 = 43 (divisible)\n49 / 7 = 7 (divisible)\nTherefore, HCF = 7.\nThe greatest number is 7.\nVerification: 54 % 7 = 5; 103 % 7 = 5; 355 % 7 = 5 (same remainder 5).",
        "kp": ["HCF of differences: |A - B|, |B - C|, |C - A|", "HCF(252, 301, 49) = 7", "Classic placement question pattern"],
        "cm": ["Trying to find HCF of the original numbers directly"],
        "fu": ["What is the common remainder (5)?"],
        "tags": ["aptitude", "quantitative", "hcf-lcm", "placement-pattern", "top-30"]
    },

    # -------------------------------------------------------------
    # SECTION B: LOGICAL REASONING (Q61 - Q105)
    # -------------------------------------------------------------
    # --- Number Series ---
    {
        "n": 61, "sub": "Logical Reasoning - Number Series", "d": "Beginner",
        "q": "Find the next number in the series: 2, 4, 8, 16, ?",
        "ans": "Pattern: Each number is multiplied by 2 (powers of 2).\n2 * 2 = 4\n4 * 2 = 8\n8 * 2 = 16\n16 * 2 = 32.\nNext number = 32.",
        "kp": ["Geometric progression with common ratio r = 2", "Next term = 32"],
        "cm": ["Adding 8"],
        "fu": ["What is the 8th term (256)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series"]
    },
    {
        "n": 62, "sub": "Logical Reasoning - Number Series", "d": "Beginner",
        "q": "Find the next number in the series: 3, 6, 12, 24, ?",
        "ans": "Pattern: Each number is multiplied by 2.\n24 * 2 = 48.\nNext number = 48.",
        "kp": ["Doubling series: 24 * 2 = 48"],
        "cm": ["Adding 12"],
        "fu": ["What is the next number after 48 (96)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series"]
    },
    {
        "n": 63, "sub": "Logical Reasoning - Number Series", "d": "Beginner",
        "q": "Find the next number in the series: 5, 10, 17, 26, 37, ?",
        "ans": "Difference analysis:\n10 - 5 = +5\n17 - 10 = +7\n26 - 17 = +9\n37 - 26 = +11\nThe differences are consecutive odd numbers: 5, 7, 9, 11.\nNext difference = +13.\nNext number = 37 + 13 = 50.\nAlternative Pattern: n^2 + 1: 2^2+1=5, 3^2+1=10, 4^2+1=17, 5^2+1=26, 6^2+1=37, 7^2+1 = 50.",
        "kp": ["Consecutive odd differences: +5, +7, +9, +11, +13", "n^2 + 1 series: 7^2 + 1 = 50"],
        "cm": ["Missing the double difference pattern"],
        "fu": ["What is the next number after 50 (8^2 + 1 = 65)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series", "top-30"]
    },
    {
        "n": 64, "sub": "Logical Reasoning - Number Series", "d": "Beginner",
        "q": "Find the next number in the series: 1, 4, 9, 16, 25, ?",
        "ans": "Pattern: Perfect squares of consecutive natural numbers.\n1^2 = 1, 2^2 = 4, 3^2 = 9, 4^2 = 16, 5^2 = 25.\nNext term = 6^2 = 36.",
        "kp": ["Square numbers series: n^2", "6^2 = 36"],
        "cm": ["Misidentifying square pattern"],
        "fu": ["What is the 10th term in this series (100)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series"]
    },
    {
        "n": 65, "sub": "Logical Reasoning - Number Series", "d": "Intermediate",
        "q": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
        "ans": "Method 1: Differences: +4, +6, +8, +10 => Next difference is +12. 30 + 12 = 42.\nMethod 2: n*(n+1) or n^2 + n:\n1*2 = 2\n2*3 = 6\n3*4 = 12\n4*5 = 20\n5*6 = 30\n6*7 = 42.\nNext number = 42.",
        "kp": ["n*(n+1) pronic numbers pattern", "Differences increasing by 2: next is +12 => 42"],
        "cm": ["Arithmetic addition mistake"],
        "fu": ["What is the 7th term in this series (7*8 = 56)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series", "top-30"]
    },
    {
        "n": 66, "sub": "Logical Reasoning - Number Series", "d": "Intermediate",
        "q": "Find the next number in the series: 100, 90, 81, 72.9, ?",
        "ans": "Pattern: Each number is multiplied by 0.9 (or decreased by 10%).\n100 * 0.9 = 90\n90 * 0.9 = 81\n81 * 0.9 = 72.9\n72.9 * 0.9 = 65.61.\nNext number = 65.61.",
        "kp": ["Common ratio r = 0.9", "72.9 * 0.9 = 65.61"],
        "cm": ["Assuming linear subtraction of 10 or 9"],
        "fu": ["What is this series called? (Decreasing Geometric Progression)."],
        "tags": ["aptitude", "logical-reasoning", "number-series"]
    },
    {
        "n": 67, "sub": "Logical Reasoning - Number Series", "d": "Beginner",
        "q": "Find the next number in the series: 7, 14, 28, 56, ?",
        "ans": "Pattern: Doubling each number (* 2).\n56 * 2 = 112.\nNext number = 112.",
        "kp": ["56 * 2 = 112"],
        "cm": ["Arithmetic mistake"],
        "fu": ["What is the next number after 112 (224)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series"]
    },
    {
        "n": 68, "sub": "Logical Reasoning - Number Series", "d": "Beginner",
        "q": "Find the next number in the series: 1, 1, 2, 3, 5, 8, ?",
        "ans": "Pattern: Fibonacci Series. Each term is the sum of the preceding two terms.\n1 + 1 = 2\n1 + 2 = 3\n2 + 3 = 5\n3 + 5 = 8\n5 + 8 = 13.\nNext number = 13.",
        "kp": ["Fibonacci series: F(n) = F(n-1) + F(n-2)", "5 + 8 = 13"],
        "cm": ["Searching for difference or multiplication patterns"],
        "fu": ["What is the next number after 13 (8 + 13 = 21)?"],
        "tags": ["aptitude", "logical-reasoning", "number-series", "fibonacci", "top-30"]
    },

    # --- Coding-Decoding ---
    {
        "n": 69, "sub": "Logical Reasoning - Coding & Decoding", "d": "Beginner",
        "q": "If CAT is coded as DBU, how is DOG coded in that language?",
        "ans": "Pattern: Each letter is shifted forward by +1 position in the alphabet.\nC (+1) -> D\nA (+1) -> B\nT (+1) -> U\nApply to DOG:\nD (+1) -> E\nO (+1) -> P\nG (+1) -> H\nCode for DOG = EPH.",
        "kp": ["Letter shift: +1 forward", "DOG -> EPH"],
        "cm": ["Shifting backward instead of forward"],
        "fu": ["How would BIRD be coded (CJSE)?"],
        "tags": ["aptitude", "logical-reasoning", "coding-decoding"]
    },
    {
        "n": 70, "sub": "Logical Reasoning - Coding & Decoding", "d": "Beginner",
        "q": "If A=1, B=2, ..., Z=26, find the numerical value of CAT.",
        "ans": "Alphabet positions:\nC = 3\nA = 1\nT = 20\nSum = 3 + 1 + 20 = 24.\nValue of CAT = 24.",
        "kp": ["C=3, A=1, T=20", "Sum = 24"],
        "cm": ["Misremembering alphabet position of T"],
        "fu": ["What is the value of DOG (4 + 15 + 7 = 26)?"],
        "tags": ["aptitude", "logical-reasoning", "coding-decoding"]
    },
    {
        "n": 71, "sub": "Logical Reasoning - Coding & Decoding", "d": "Beginner",
        "q": "If PEN is coded as QFO, what is the code for BOOK?",
        "ans": "Pattern: Each letter is shifted by +1.\nP (+1) -> Q\nE (+1) -> F\nN (+1) -> O\nApply to BOOK:\nB (+1) -> C\nO (+1) -> P\nO (+1) -> P\nK (+1) -> L\nCode for BOOK = CPPL.",
        "kp": ["Letter shift +1", "BOOK -> CPPL"],
        "cm": ["Shifting only vowels"],
        "fu": ["How is DESK coded (EFTL)?"],
        "tags": ["aptitude", "logical-reasoning", "coding-decoding"]
    },
    {
        "n": 72, "sub": "Logical Reasoning - Coding & Decoding", "d": "Beginner",
        "q": "If APPLE is coded as ELPPA, what is the coding method used?",
        "ans": "Pattern: The letters of the word are written in completely reversed order.\nA-P-P-L-E reversed is E-L-P-P-A.\nCoding method: String Reversal.",
        "kp": ["Reversal coding pattern", "APPLE -> ELPPA"],
        "cm": ["Overcomplicating with alphabet numerical shifts"],
        "fu": ["How would ORANGE be coded in this method (EGNARO)?"],
        "tags": ["aptitude", "logical-reasoning", "coding-decoding"]
    },
    {
        "n": 73, "sub": "Logical Reasoning - Coding & Decoding", "d": "Beginner",
        "q": "If ROAD is coded as URDG, what is the pattern of coding?",
        "ans": "Pattern: Each letter is shifted forward by +3 positions in the alphabet.\nR (+3) -> U (18 -> 21)\nO (+3) -> R (15 -> 18)\nA (+3) -> D (1 -> 4)\nD (+3) -> G (4 -> 7)\nPattern: +3 Alphabet Shift.",
        "kp": ["Shift pattern: +3 forward on all characters"],
        "cm": ["Miscalculating the shift distance"],
        "fu": ["Using this rule, what is the code for SWAN (VZDQ)?"],
        "tags": ["aptitude", "logical-reasoning", "coding-decoding"]
    },

    # --- Blood Relations ---
    {
        "n": 74, "sub": "Logical Reasoning - Blood Relations", "d": "Beginner",
        "q": "Ravi says, 'She is the daughter of my mother\\'s only son.' Who is she to Ravi?",
        "ans": "Break down from the end:\n1) 'My mother\\'s only son': Since Ravi is speaking, his mother's only son is Ravi himself.\n2) 'The daughter of [Ravi]': Ravi's daughter.\nAnswer: She is Ravi's daughter.",
        "kp": ["Mother's only son = Self (for male narrator Ravi)", "Daughter of self = Daughter"],
        "cm": ["Confusing 'only son' with brother"],
        "fu": ["If a woman said 'He is the son of my mother\\'s only daughter', who is he? (Her son)."],
        "tags": ["aptitude", "logical-reasoning", "blood-relations", "top-30"]
    },
    {
        "n": 75, "sub": "Logical Reasoning - Blood Relations", "d": "Beginner",
        "q": "A is B's brother. C is B's mother. D is C's father. What is D to A?",
        "ans": "Relationship Chain:\n- A and B are siblings (A is brother of B).\n- C is mother of B, therefore C is also the mother of A.\n- D is father of C (mother's father).\nMother's father is Maternal Grandfather.\nAnswer: Grandfather (Maternal Grandfather).",
        "kp": ["A's mother is C", "C's father D is A's Maternal Grandfather"],
        "cm": ["Confusing paternal grandfather with maternal grandfather"],
        "fu": ["What is A to D? (Grandson)."],
        "tags": ["aptitude", "logical-reasoning", "blood-relations"]
    },
    {
        "n": 76, "sub": "Logical Reasoning - Blood Relations", "d": "Beginner",
        "q": "Pointing to a man, Priya says, 'He is the son of my grandfather\\'s only son.' Who is the man to Priya?",
        "ans": "Step-by-step resolution:\n1) 'My grandfather\\'s only son': Priya's paternal grandfather's only son is Priya's father.\n2) 'The son of my father': Priya's brother (or self, but narrator is female Priya pointing to a man).\nAnswer: He is Priya's brother.",
        "kp": ["Grandfather's only son = Father", "Son of father = Brother"],
        "cm": ["Assuming cousin (the word 'only' eliminates other uncles)"],
        "fu": ["What if Priya's grandfather had two sons?"],
        "tags": ["aptitude", "logical-reasoning", "blood-relations", "top-30"]
    },
    {
        "n": 77, "sub": "Logical Reasoning - Blood Relations", "d": "Beginner",
        "q": "X is the sister of Y. Y is the father of Z. What is X to Z?",
        "ans": "Relationship Chain:\n- Y is the father of Z.\n- X is the sister of Y (father's sister).\nFather's sister is Paternal Aunt.\nAnswer: Aunt.",
        "kp": ["Father's sister = Aunt"],
        "cm": ["Confusing aunt with mother or niece"],
        "fu": ["What is Z to X? (Niece or Nephew, depending on gender of Z)."],
        "tags": ["aptitude", "logical-reasoning", "blood-relations"]
    },

    # --- Direction Sense ---
    {
        "n": 78, "sub": "Logical Reasoning - Direction Sense", "d": "Beginner",
        "q": "A person walks 5 km North, then turns and walks 3 km East. In which direction is he from the starting point?",
        "ans": "Vector Analysis:\n- North is upward on the Y-axis (+5).\n- East is rightward on the X-axis (+3).\nPosition relative to origin (0,0) is (+3, +5), which lies in the North-East quadrant.\nAnswer: North-East.",
        "kp": ["North + East movement = North-East direction from start"],
        "cm": ["Saying East or North instead of composite diagonal direction"],
        "fu": ["What is the direct straight-line distance? (sqrt(25 + 9) = sqrt(34) km)."],
        "tags": ["aptitude", "logical-reasoning", "direction-sense"]
    },
    {
        "n": 79, "sub": "Logical Reasoning - Direction Sense", "d": "Beginner",
        "q": "A person walks 10 km East, then turns around and walks 10 km West. What is his distance from the starting point?",
        "ans": "Opposite movements along the same axis cancel each other out:\n+10 km East + (-10 km West) = 0 km.\nDistance from start = 0 km (he is back at the starting point).",
        "kp": ["Displacement is 0 km", "Returned to origin"],
        "cm": ["Calculating total distance traveled (20 km) instead of distance from start (displacement = 0)"],
        "fu": ["What is the total distance walked? (20 km)."],
        "tags": ["aptitude", "logical-reasoning", "direction-sense"]
    },
    {
        "n": 80, "sub": "Logical Reasoning - Direction Sense", "d": "Beginner",
        "q": "Facing North, a person turns right, then turns left, then turns right. What is his final facing direction?",
        "ans": "Turn sequence starting facing North:\n1) Turn right (90° clockwise): Facing East.\n2) Turn left (90° counter-clockwise): Facing North.\n3) Turn right (90° clockwise): Facing East.\nFinal direction = East.",
        "kp": ["Right and Left cancel: (Right + Left + Right) = Net Right turn", "North + Right turn = East"],
        "cm": ["Turning in the wrong clockwise direction"],
        "fu": ["What if he took three consecutive right turns from North? (West)."],
        "tags": ["aptitude", "logical-reasoning", "direction-sense"]
    },
    {
        "n": 81, "sub": "Logical Reasoning - Direction Sense", "d": "Beginner",
        "q": "A person travels 4 km North and then 3 km East. What is the shortest straight-line distance from the starting point?",
        "ans": "Use the Pythagorean Theorem (Right-angled triangle):\nDistance = sqrt((North)^2 + (East)^2)\nDistance = sqrt(4^2 + 3^2) = sqrt(16 + 9) = sqrt(25) = 5 km.\nShortest distance = 5 km (classic 3-4-5 Pythagorean triplet).",
        "kp": ["Pythagorean theorem: sqrt(3^2 + 4^2) = 5 km", "3-4-5 triplet"],
        "cm": ["Adding 4 + 3 = 7 km (that is total path length, not shortest displacement)"],
        "fu": ["What if he traveled 6 km North and 8 km East? (10 km)."],
        "tags": ["aptitude", "logical-reasoning", "direction-sense", "pythagoras", "top-30"]
    },
    {
        "n": 82, "sub": "Logical Reasoning - Direction Sense", "d": "Beginner",
        "q": "Facing South, you turn to your left. Which direction are you now facing?",
        "ans": "Facing South means looking downward.\nA left turn is counter-clockwise (90°).\nFrom South, a left turn points towards East.\nAnswer: East.",
        "kp": ["Facing South: Left is East, Right is West"],
        "cm": ["Confusing own left with compass left while facing South"],
        "fu": ["Facing West, if you turn right, which direction do you face? (North)."],
        "tags": ["aptitude", "logical-reasoning", "direction-sense"]
    },

    # --- Syllogism ---
    {
        "n": 83, "sub": "Logical Reasoning - Syllogism", "d": "Beginner",
        "q": "Statements: All cats are animals. All animals are living beings.\nConclusion: All cats are living beings. Is this conclusion True or False?",
        "ans": "Venn diagram deduction:\n- Circle 'Cats' is completely inside circle 'Animals'.\n- Circle 'Animals' is completely inside circle 'Living beings'.\nTherefore, circle 'Cats' is completely inside circle 'Living beings'.\nConclusion is 100% Valid / True.",
        "kp": ["Transitive property of universal affirmative propositions (All A are B, All B are C => All A are C)", "Conclusion is True"],
        "cm": ["Overthinking outside real-world definitions"],
        "fu": ["Can we conclude: All living beings are cats? (No, invalid)."],
        "tags": ["aptitude", "logical-reasoning", "syllogisms", "top-30"]
    },
    {
        "n": 84, "sub": "Logical Reasoning - Syllogism", "d": "Intermediate",
        "q": "Statements: All A are B. Some B are C.\nConclusion: Some A are C. Can this conclusion be definitely deduced?",
        "ans": "Venn Diagram Analysis:\n- Set A is entirely inside Set B.\n- Set C intersects with Set B.\n- However, Set C might intersect only with the part of B outside A, without touching A at all.\nSince there is no guaranteed overlap between A and C, the conclusion 'Some A are C' cannot be definitely concluded.\nAnswer: Cannot be concluded (Invalid).",
        "kp": ["Intersection between B and C does not guarantee intersection with subset A", "Cannot be definitely concluded"],
        "cm": ["Assuming that because A is in B, it must touch C"],
        "fu": ["What if the statement added: 'All B are C'? (Then All A are C would be valid)."],
        "tags": ["aptitude", "logical-reasoning", "syllogisms", "top-30"]
    },
    {
        "n": 85, "sub": "Logical Reasoning - Syllogism", "d": "Intermediate",
        "q": "Statements: No apples are oranges. Some fruits are apples.\nConclusion: Some fruits are not oranges. Is this conclusion True?",
        "ans": "Deduction:\n- There are some fruits that are apples.\n- But NO apples can be oranges.\n- Therefore, those specific fruits that are apples can never be oranges.\nHence, 'Some fruits are not oranges' is definitely TRUE.\nAnswer: True (Valid).",
        "kp": ["Those fruits which are apples cannot be oranges", "Conclusion is definitely True"],
        "cm": ["Assuming negative conclusions are always false"],
        "fu": ["Can we conclude that 'Some fruits are oranges'? (No, undetermined)."],
        "tags": ["aptitude", "logical-reasoning", "syllogisms"]
    },
    {
        "n": 86, "sub": "Logical Reasoning - Syllogism", "d": "Beginner",
        "q": "Statements: All engineers are graduates. Ravi is an engineer.\nConclusion: What can be concluded about Ravi?",
        "ans": "Deduction:\n- Ravi belongs to the set 'engineers'.\n- All members of 'engineers' belong to the set 'graduates'.\nTherefore, Ravi is a graduate.\nConclusion: Ravi is a graduate.",
        "kp": ["Direct syllogistic deduction: Ravi is a graduate"],
        "cm": ["Saying no conclusion can be drawn"],
        "fu": ["If Shyam is a graduate, can we conclude Shyam is an engineer? (No, undistributed middle)."],
        "tags": ["aptitude", "logical-reasoning", "syllogisms"]
    },
    {
        "n": 87, "sub": "Logical Reasoning - Syllogism", "d": "Beginner",
        "q": "Statements: Some A are B. Some B are C.\nCan we definitely conclude that Some A are C?",
        "ans": "Analysis:\nTwo particular premises ('Some' + 'Some') yield NO definite conclusion connecting the extreme terms A and C.\nSet A overlaps with B, and Set C overlaps with B, but A and C may be completely disjoint.\nAnswer: No (Cannot be concluded).",
        "kp": ["Two 'Some' statements yield no definite conclusion", "A and C might have zero overlap"],
        "cm": ["Assuming chaining works on 'Some' premises"],
        "fu": ["Can we conclude: 'Some A may be C' (possibility)? (Yes, possible, but not definite)."],
        "tags": ["aptitude", "logical-reasoning", "syllogisms"]
    },

    # --- Analogy / Odd One Out ---
    {
        "n": 88, "sub": "Logical Reasoning - Analogy & Odd One Out", "d": "Beginner",
        "q": "Complete the analogy: Doctor : Hospital :: Teacher : ?",
        "ans": "Relationship: Professional to their primary workplace.\nA Doctor works in a Hospital.\nSimilarly, a Teacher works in a School.\nAnswer: School.",
        "kp": ["Worker : Workplace relationship", "Teacher works in a School"],
        "cm": ["Picking Student (that is client/receiver, not workplace)"],
        "fu": ["Lawyer : ? (Court)."],
        "tags": ["aptitude", "logical-reasoning", "analogies"]
    },
    {
        "n": 89, "sub": "Logical Reasoning - Analogy & Odd One Out", "d": "Beginner",
        "q": "Complete the analogy: Bird : Fly :: Fish : ?",
        "ans": "Relationship: Animal to its characteristic primary mode of locomotion.\nA Bird moves by Flying.\nA Fish moves by Swimming.\nAnswer: Swim.",
        "kp": ["Creature : Locomotion relationship", "Fish : Swim"],
        "cm": ["Picking Water (that is medium/habitat, not action)"],
        "fu": ["Snake : ? (Crawl)."],
        "tags": ["aptitude", "logical-reasoning", "analogies"]
    },
    {
        "n": 90, "sub": "Logical Reasoning - Analogy & Odd One Out", "d": "Beginner",
        "q": "Find the odd one out: Apple, Mango, Carrot, Banana.",
        "ans": "Categorization:\n- Apple, Mango, and Banana are Fruits.\n- Carrot is a Vegetable (and a root tuber).\nAnswer: Carrot.",
        "kp": ["Carrot is a root vegetable; others are fruits"],
        "cm": ["Focusing on color differences instead of biological classification"],
        "fu": ["Find odd one: Potato, Onion, Tomato, Ginger (Tomato is a fruit/grows above ground)."],
        "tags": ["aptitude", "logical-reasoning", "odd-one-out"]
    },
    {
        "n": 91, "sub": "Logical Reasoning - Analogy & Odd One Out", "d": "Beginner",
        "q": "Find the odd one out: 2, 3, 5, 9, 11.",
        "ans": "Classification by prime numbers:\n- 2, 3, 5, 11 are all Prime Numbers.\n- 9 is a Composite Number (3 * 3 = 9).\nAnswer: 9.",
        "kp": ["9 is composite; all others are prime numbers"],
        "cm": ["Thinking 2 is odd one out because it's even"],
        "fu": ["Find odd one: 11, 13, 15, 17 (15 is composite)."],
        "tags": ["aptitude", "logical-reasoning", "odd-one-out", "primes"]
    },
    {
        "n": 92, "sub": "Logical Reasoning - Analogy & Odd One Out", "d": "Beginner",
        "q": "Complete the analogy: Book : Reading :: Food : ?",
        "ans": "Relationship: Object to its primary intended consumption action.\nA Book is consumed by Reading.\nFood is consumed by Eating.\nAnswer: Eating.",
        "kp": ["Object : Action relationship", "Food : Eating"],
        "cm": ["Picking Cooking (that is preparation, not primary consumption)"],
        "fu": ["Song : ? (Listening)."],
        "tags": ["aptitude", "logical-reasoning", "analogies"]
    },

    # --- Seating Arrangement ---
    {
        "n": 93, "sub": "Logical Reasoning - Seating Arrangement", "d": "Beginner",
        "q": "Five people A, B, C, D, E sit in a row facing north. A is to the left of B, and B is to the left of C. Who is definitely not seated before A?",
        "ans": "Arrangement ordering: ... A ... B ... C ...\nSince B is to the right of A, and C is to the right of B, both B and C are seated after A.\nTherefore, neither B nor C can definitely be seated before A.\nAnswer: B and C.",
        "kp": ["Left-to-right ordering: A precedes B, B precedes C", "B and C are definitely not before A"],
        "cm": ["Overlooking C's dependency on B"],
        "fu": ["Can D be seated before A? (Yes, possible)."],
        "tags": ["aptitude", "logical-reasoning", "seating-arrangement"]
    },
    {
        "n": 94, "sub": "Logical Reasoning - Seating Arrangement", "d": "Beginner",
        "q": "A is immediately to the left of B. C is immediately to the right of B. What is their linear arrangement?",
        "ans": "Analysis:\n- 'A is immediately left of B' gives sub-block: [A, B]\n- 'C is immediately right of B' places C directly after B: [B, C]\nCombining both gives: A - B - C.\nAnswer: A - B - C.",
        "kp": ["Immediate neighbors: A on left, C on right of B => A-B-C"],
        "cm": ["Inverting left and right"],
        "fu": ["If D sits immediately left of A, what is the 4-person arrangement? (D-A-B-C)."],
        "tags": ["aptitude", "logical-reasoning", "seating-arrangement"]
    },
    {
        "n": 95, "sub": "Logical Reasoning - Seating Arrangement", "d": "Beginner",
        "q": "P is seated between Q and R. What are the possible linear arrangements?",
        "ans": "Since P is between Q and R, P is in the center with Q and R at the flanking positions.\nTwo symmetrical possibilities exist:\n1) Q - P - R\n2) R - P - Q\nAnswer: Q-P-R or R-P-Q.",
        "kp": ["Two valid arrangements: Q-P-R or R-P-Q depending on orientation"],
        "cm": ["Assuming Q must always be on the left"],
        "fu": ["If Q is to the left of R, which arrangement is unique? (Q-P-R)."],
        "tags": ["aptitude", "logical-reasoning", "seating-arrangement"]
    },
    {
        "n": 96, "sub": "Logical Reasoning - Seating Arrangement", "d": "Beginner",
        "q": "Five people sit in a row. A is at the extreme left and E is at the extreme right. How many people are seated between them?",
        "ans": "Row positions: 1, 2, 3, 4, 5.\nPosition 1 = A (extreme left).\nPosition 5 = E (extreme right).\nThe intermediate positions are 2, 3, and 4.\nTotal people between them = 3 people.\nAnswer: 3.",
        "kp": ["5 total - 2 endpoints = 3 intermediate positions"],
        "cm": ["Subtracting 5 - 1 = 4 without excluding the second endpoint"],
        "fu": ["If 8 people sit in a row with ends fixed, how many are between them? (6)."],
        "tags": ["aptitude", "logical-reasoning", "seating-arrangement"]
    },
    {
        "n": 97, "sub": "Logical Reasoning - Seating Arrangement", "d": "Intermediate",
        "q": "In a circular arrangement of 8 people facing center, A sits diametrically opposite to B. How many people are seated between them along either side?",
        "ans": "In a circle of N people, the number of people between two diametrically opposite seats along either path is:\nBetween = (N - 2) / 2\nFor N = 8:\nBetween = (8 - 2) / 2 = 6 / 2 = 3 people.\nThere are exactly 3 people seated between A and B on both the left and right sides.\nAnswer: 3.",
        "kp": ["Circular opposite seats: (N - 2) / 2", "For 8 people, exactly 3 on each side"],
        "cm": ["Saying 4 people"],
        "fu": ["In a circle of 10 people, how many sit between opposite seats? (4)."],
        "tags": ["aptitude", "logical-reasoning", "circular-arrangement", "top-30"]
    },

    # --- Ranking ---
    {
        "n": 98, "sub": "Logical Reasoning - Ranking", "d": "Beginner",
        "q": "Ravi is ranked 7th from the top and 14th from the bottom in a class. What is the total number of students?",
        "ans": "Ranking Formula: Total = Rank from Top + Rank from Bottom - 1\n(The -1 is necessary because Ravi is counted twice: once from the top, once from the bottom).\nTotal = 7 + 14 - 1 = 21 - 1 = 20 students.\nAnswer: 20 students.",
        "kp": ["Formula: Total = Top + Bottom - 1", "7 + 14 - 1 = 20"],
        "cm": ["Forgetting the -1 and answering 21"],
        "fu": ["If Priya is 10th from top and 20th from bottom, what is the total? (29)."],
        "tags": ["aptitude", "logical-reasoning", "ranking", "top-30"]
    },
    {
        "n": 99, "sub": "Logical Reasoning - Ranking", "d": "Beginner",
        "q": "In a row of 30 students, A is 10th from the left. What is A's position from the right end?",
        "ans": "Formula: Position from Right = Total - Position from Left + 1\nPosition from Right = 30 - 10 + 1 = 20 + 1 = 21st.\nAnswer: 21st.",
        "kp": ["Formula: Right = Total - Left + 1", "30 - 10 + 1 = 21st"],
        "cm": ["Subtracting 30 - 10 = 20th without adding 1"],
        "fu": ["What is the position from left if a person is 15th from right in a row of 40? (26th)."],
        "tags": ["aptitude", "logical-reasoning", "ranking"]
    },
    {
        "n": 100, "sub": "Logical Reasoning - Ranking", "d": "Beginner",
        "q": "In an ordered rank list, A ranks 5th and B ranks 8th. How many people are ranked between them?",
        "ans": "Formula: People Between = Higher Rank - Lower Rank - 1\nPeople Between = 8 - 5 - 1 = 3 - 1 = 2.\nThe people between them are ranks 6 and 7 (2 people).\nAnswer: 2.",
        "kp": ["People between = (8 - 5) - 1 = 2 (ranks 6 and 7)"],
        "cm": ["Subtracting 8 - 5 = 3 without subtracting 1"],
        "fu": ["How many people are between rank 12 and rank 20? (7)."],
        "tags": ["aptitude", "logical-reasoning", "ranking"]
    },
    {
        "n": 101, "sub": "Logical Reasoning - Ranking", "d": "Beginner",
        "q": "A is taller than B, but shorter than C. Who is the tallest among them?",
        "ans": "Height inequality:\n- 'A is taller than B' => A > B\n- 'A is shorter than C' => C > A\nCombining inequalities: C > A > B.\nTherefore, C is the tallest.\nAnswer: C.",
        "kp": ["Inequality chain: C > A > B", "C is tallest; B is shortest"],
        "cm": ["Misinterpreting 'shorter than'"],
        "fu": ["Who is the shortest? (B)."],
        "tags": ["aptitude", "logical-reasoning", "comparison"]
    },

    # --- Clock & Calendar ---
    {
        "n": 102, "sub": "Logical Reasoning - Clock & Calendar", "d": "Beginner",
        "q": "How many degrees does the minute hand of a clock move in 10 minutes?",
        "ans": "In 60 minutes, the minute hand completes a full circle (360°).\nSpeed of minute hand = 360° / 60 min = 6° per minute.\nIn 10 minutes: 10 * 6° = 60°.\nAnswer: 60°.",
        "kp": ["Minute hand speed = 6° per minute", "10 min * 6° = 60°"],
        "cm": ["Using hour hand speed (0.5°/min) instead of minute hand"],
        "fu": ["How many degrees in 25 minutes? (150°)."],
        "tags": ["aptitude", "logical-reasoning", "clocks", "top-30"]
    },
    {
        "n": 103, "sub": "Logical Reasoning - Clock & Calendar", "d": "Beginner",
        "q": "How many degrees does the hour hand of a clock move in 2 hours?",
        "ans": "In 12 hours, the hour hand completes a full circle (360°).\nSpeed of hour hand = 360° / 12 h = 30° per hour (or 0.5° per minute).\nIn 2 hours: 2 * 30° = 60°.\nAnswer: 60°.",
        "kp": ["Hour hand speed = 30° per hour (0.5° per minute)", "2 hours * 30° = 60°"],
        "cm": ["Confusing hour hand with minute hand"],
        "fu": ["How many degrees does the hour hand move in 30 minutes? (15°)."],
        "tags": ["aptitude", "logical-reasoning", "clocks"]
    },
    {
        "n": 104, "sub": "Logical Reasoning - Clock & Calendar", "d": "Beginner",
        "q": "If today is Monday, what day of the week will it be after 10 days?",
        "ans": "Days repeat in cycles of 7 (mod 7 arithmetic).\nOdd days = 10 mod 7 = 3 days ahead.\nStarting from Monday:\n+1 day = Tuesday\n+2 days = Wednesday\n+3 days = Thursday.\nAnswer: Thursday.",
        "kp": ["Odd days = 10 % 7 = 3", "Monday + 3 = Thursday"],
        "cm": ["Counting today as day 1"],
        "fu": ["What day will it be after 100 days? (100 % 7 = 2 => Wednesday)."],
        "tags": ["aptitude", "logical-reasoning", "calendar", "odd-days", "top-30"]
    },
    {
        "n": 105, "sub": "Logical Reasoning - Clock & Calendar", "d": "Beginner",
        "q": "How many odd days are there in a normal (non-leap) calendar year?",
        "ans": "A normal year has 365 days.\nDivide by 7: 365 / 7 = 52 weeks and 1 remainder day.\n52 * 7 = 364 days.\nRemaining day = 365 - 364 = 1 odd day.\n(A leap year has 366 days => 366 % 7 = 2 odd days).\nAnswer: 1 odd day.",
        "kp": ["Normal year (365 days) = 52 weeks + 1 odd day", "Leap year (366 days) = 52 weeks + 2 odd days"],
        "cm": ["Saying 0 or 2 for a normal year"],
        "fu": ["How many odd days are in 100 years? (5 odd days)."],
        "tags": ["aptitude", "logical-reasoning", "calendar", "odd-days"]
    },

    # -------------------------------------------------------------
    # SECTION C: VERBAL ABILITY (Q106 - Q130)
    # -------------------------------------------------------------
    {
        "n": 106, "sub": "Verbal Ability - Vocabulary", "d": "Beginner",
        "q": "Choose the synonym of 'Abundant'.",
        "ans": "Definition: 'Abundant' means existing or available in large quantities; more than enough.\nSynonyms: Plentiful, Copious, Ample, Bountiful.\nAnswer: Plentiful.",
        "kp": ["Abundant = Plentiful / Ample", "Antonym is Scarce"],
        "cm": ["Confusing with Abandoned"],
        "fu": ["Use 'abundant' in a sentence about natural resources."],
        "tags": ["aptitude", "verbal-ability", "synonyms"]
    },
    {
        "n": 107, "sub": "Verbal Ability - Vocabulary", "d": "Beginner",
        "q": "What is the antonym of 'Ancient'?",
        "ans": "Definition: 'Ancient' means belonging to the very distant past; no longer in existence.\nAntonyms: Modern, Contemporary, Recent, Current.\nAnswer: Modern.",
        "kp": ["Ancient <-> Modern / Contemporary"],
        "cm": ["Picking antique (which is a synonym)"],
        "fu": ["What is the difference between ancient and antique?"],
        "tags": ["aptitude", "verbal-ability", "antonyms"]
    },
    {
        "n": 108, "sub": "Verbal Ability - Vocabulary", "d": "Beginner",
        "q": "Choose the synonym of 'Brief'.",
        "ans": "Definition: 'Brief' means of short duration or concise in expression.\nSynonyms: Short, Concise, Succinct, Fleeting.\nAnswer: Short.",
        "kp": ["Brief = Short / Concise"],
        "cm": ["Confusing brief with grief"],
        "fu": ["What is the antonym of brief? (Prolonged / Lengthy)."],
        "tags": ["aptitude", "verbal-ability", "synonyms"]
    },
    {
        "n": 109, "sub": "Verbal Ability - Vocabulary", "d": "Beginner",
        "q": "What is the antonym of 'Expand'?",
        "ans": "Definition: 'Expand' means to become or make larger or more extensive.\nAntonyms: Contract, Shrink, Compress, Condense.\nAnswer: Contract.",
        "kp": ["Expand <-> Contract / Shrink"],
        "cm": ["Picking extend (which is a synonym)"],
        "fu": ["What does thermal expansion and contraction mean in physics?"],
        "tags": ["aptitude", "verbal-ability", "antonyms"]
    },
    {
        "n": 110, "sub": "Verbal Ability - Vocabulary", "d": "Beginner",
        "q": "Choose the synonym of 'Candid'.",
        "ans": "Definition: 'Candid' means truthful, straightforward, and frank in speech or manner.\nSynonyms: Frank, Honest, Outspoken, Forthright, Direct.\nAnswer: Frank / Honest.",
        "kp": ["Candid = Frank / Honest / Forthright", "Antonym is Deceitful / Secretive"],
        "cm": ["Associating only with unposed 'candid photos'"],
        "fu": ["What does a 'candid confession' mean?"],
        "tags": ["aptitude", "verbal-ability", "synonyms"]
    },
    {
        "n": 111, "sub": "Verbal Ability - Vocabulary", "d": "Beginner",
        "q": "What is the antonym of 'Scarce'?",
        "ans": "Definition: 'Scarce' means insufficient for the demand; rare.\nAntonyms: Abundant, Plentiful, Copious, Plenteous.\nAnswer: Abundant.",
        "kp": ["Scarce <-> Abundant / Plentiful"],
        "cm": ["Picking rare (which is a synonym)"],
        "fu": ["What is scarcity in economics?"],
        "tags": ["aptitude", "verbal-ability", "antonyms"]
    },
    {
        "n": 112, "sub": "Verbal Ability - Grammar", "d": "Beginner",
        "q": "Fill in the blank: 'He ___ to college every day.' (go / goes / going / gone)",
        "ans": "Subject-Verb Agreement & Tense:\n'Every day' indicates a habitual action requiring the Simple Present Tense.\nThe subject 'He' is third-person singular, which takes the singular verb form ending in -s/es ('goes').\nAnswer: goes ('He goes to college every day.').",
        "kp": ["Habitual present action uses Simple Present Tense", "Third-person singular 'He' takes 'goes'"],
        "cm": ["Using base form 'go' with third person singular"],
        "fu": ["What would be the correct verb if the subject was 'They'? ('go')."],
        "tags": ["aptitude", "verbal-ability", "grammar", "tenses"]
    },
    {
        "n": 113, "sub": "Verbal Ability - Grammar", "d": "Beginner",
        "q": "Fill in the blank: 'Neither Ram nor Shyam ___ present.' (is / are / were / have)",
        "ans": "Subject-Verb Agreement Rule:\nWhen two singular subjects are connected by 'Neither... nor' or 'Either... or', the verb agrees with the closer subject (or takes a singular verb if both are singular).\nHere, 'Shyam' is singular, so the verb must be singular 'is'.\nAnswer: is ('Neither Ram nor Shyam is present.').",
        "kp": ["Neither... nor with singular subjects takes a singular verb 'is'", "Proximity rule in compound correlative conjunctions"],
        "cm": ["Treating 'Neither... nor' as plural like 'and'"],
        "fu": ["What if it was: 'Neither the teacher nor the students ___ present'? ('were/are')."],
        "tags": ["aptitude", "verbal-ability", "grammar", "subject-verb-agreement", "top-30"]
    },
    {
        "n": 114, "sub": "Verbal Ability - Prepositions", "d": "Beginner",
        "q": "Fill in the blank: 'She has been working here ___ 2022.' (for / since / from / in)",
        "ans": "Prepositions of Time Rule:\n- 'Since' is used with a specific point in time (e.g., since 2022, since Monday, since 9 AM).\n- 'For' is used with a duration or period of time (e.g., for 3 years, for 5 hours).\nSince '2022' is a specific starting point in time, use 'since'.\nAnswer: since ('She has been working here since 2022.').",
        "kp": ["'Since' = specific point in time", "'For' = duration of time"],
        "cm": ["Using 'for 2022'"],
        "fu": ["Fill in: 'She has been working here ___ 3 years.' ('for')."],
        "tags": ["aptitude", "verbal-ability", "prepositions", "top-30"]
    },
    {
        "n": 115, "sub": "Verbal Ability - Prepositions", "d": "Beginner",
        "q": "Fill in the blank: 'I am interested ___ AI.' (on / at / in / with)",
        "ans": "Collocation / Fixed Preposition:\nThe adjective 'interested' is always paired with the preposition 'in'.\nAnswer: in ('I am interested in AI.').",
        "kp": ["Fixed preposition: interested in"],
        "cm": ["Using 'interested on' or 'interested with'"],
        "fu": ["What preposition pairs with 'good'? ('good at')."],
        "tags": ["aptitude", "verbal-ability", "prepositions"]
    },
    {
        "n": 116, "sub": "Verbal Ability - Sentence Correction", "d": "Beginner",
        "q": "Correct the sentence: 'He don\\'t know the answer.'",
        "ans": "Error: 'don\\'t' is the contraction of 'do not', used with plural subjects and I/You.\nFor third-person singular subjects ('He', 'She', 'It'), the correct auxiliary verb is 'does not' ('doesn\\'t').\nCorrect Sentence: 'He doesn\\'t know the answer.'",
        "kp": ["Third person singular takes 'does not' / 'doesn't'", "He doesn't know the answer"],
        "cm": ["Using 'don't' with third person singular"],
        "fu": ["Correct: 'She don't like apples.' ('She doesn't like apples')."],
        "tags": ["aptitude", "verbal-ability", "sentence-correction"]
    },
    {
        "n": 117, "sub": "Verbal Ability - Sentence Correction", "d": "Beginner",
        "q": "Correct the sentence: 'She is senior than me.'",
        "ans": "Grammar Rule: Latin comparative adjectives ending in '-ior' (senior, junior, prior, superior, inferior) are followed by the preposition 'to', never 'than'.\nCorrect Sentence: 'She is senior to me.'",
        "kp": ["Latin comparatives (senior, junior, superior, inferior) take 'to', not 'than'"],
        "cm": ["Using 'than' with senior/junior (classic error in Indian campus tests)"],
        "fu": ["Correct: 'This product is superior than that.' ('superior to that')."],
        "tags": ["aptitude", "verbal-ability", "sentence-correction", "latin-comparatives", "top-30"]
    },
    {
        "n": 118, "sub": "Verbal Ability - Sentence Correction", "d": "Beginner",
        "q": "Correct the sentence: 'Each students has a book.'",
        "ans": "Grammar Rule: The distributive adjective 'Each' is always followed by a singular countable noun and a singular verb.\n'students' (plural) must be replaced by 'student' (singular).\nCorrect Sentence: 'Each student has a book.'",
        "kp": ["'Each' is followed by a singular noun: Each student has a book"],
        "cm": ["Using plural noun after 'each'"],
        "fu": ["What if it was 'Each of the students'? (Then plural noun is used: 'Each of the students has a book')."],
        "tags": ["aptitude", "verbal-ability", "sentence-correction"]
    },
    {
        "n": 119, "sub": "Verbal Ability - Sentence Correction", "d": "Beginner",
        "q": "Correct the sentence: 'I have completed my work yesterday.'",
        "ans": "Grammar Rule: Present Perfect Tense ('have completed') cannot be used with a specific past time adverb ('yesterday', 'last week', 'in 2020'). Such sentences require the Simple Past Tense ('completed').\nCorrect Sentence: 'I completed my work yesterday.'",
        "kp": ["Specific past time markers ('yesterday', 'in 2021') require Simple Past, not Present Perfect"],
        "cm": ["Mixing present perfect with definite past time markers"],
        "fu": ["When is 'I have completed my work' correct? (When no specific past time is mentioned)."],
        "tags": ["aptitude", "verbal-ability", "sentence-correction", "tenses", "top-30"]
    },
    {
        "n": 120, "sub": "Verbal Ability - Sentence Correction", "d": "Beginner",
        "q": "Correct the sentence: 'One of my friend is a doctor.'",
        "ans": "Grammar Rule: The construction 'One of the / One of my' refers to a single individual chosen from a group, so it must be followed by a PLURAL noun and a SINGULAR verb.\n'friend' must be plural 'friends'.\nCorrect Sentence: 'One of my friends is a doctor.'",
        "kp": ["'One of + plural noun + singular verb'", "One of my friends is a doctor"],
        "cm": ["Using singular noun 'friend' or plural verb 'are'"],
        "fu": ["Correct: 'One of the car are damaged.' ('One of the cars is damaged')."],
        "tags": ["aptitude", "verbal-ability", "sentence-correction", "top-30"]
    },

    # --- Sentence Completion ---
    {
        "n": 121, "sub": "Verbal Ability - Sentence Completion", "d": "Beginner",
        "q": "Complete the sentence: 'Despite the heavy rain, the match ___ .'",
        "ans": "The conjunction 'Despite' indicates a concession or contrast. The second clause must present an outcome that contrasts with the hindrance of rain.\nCorrect continuation: 'continued' (or 'was not cancelled').\nSentence: 'Despite the heavy rain, the match continued.'",
        "kp": ["'Despite' introduces contrasting result"],
        "cm": ["Using a non-contrasting verb like 'stopped'"],
        "fu": ["What word follows 'in spite'? ('of' -> In spite of)."],
        "tags": ["aptitude", "verbal-ability", "sentence-completion"]
    },
    {
        "n": 122, "sub": "Verbal Ability - Sentence Completion", "d": "Intermediate",
        "q": "Complete the conditional sentence: 'If I had known about the problem, I ___ helped you.'",
        "ans": "Third Conditional (Unreal Past Condition) Structure:\nIf + Past Perfect ('had known'), Subject + would have + Past Participle ('would have helped').\nAnswer: would have ('If I had known about the problem, I would have helped you.').",
        "kp": ["Third conditional: 'If + had + V3' requires 'would have + V3' in the main clause"],
        "cm": ["Using 'would helped' or 'will have helped'"],
        "fu": ["What is the second conditional structure? (If + past simple, would + base verb)."],
        "tags": ["aptitude", "verbal-ability", "conditionals", "top-30"]
    },
    {
        "n": 123, "sub": "Verbal Ability - Sentence Completion", "d": "Beginner",
        "q": "Complete the sentence: 'The project was successful because the team worked ___ .' (efficient / efficiently / efficiency)",
        "ans": "An adverb is required to modify the verb 'worked'.\n'efficient' is an adjective, 'efficiency' is a noun, and 'efficiently' is an adverb of manner.\nAnswer: efficiently ('The project was successful because the team worked efficiently.').",
        "kp": ["Adverbs modify verbs: worked efficiently"],
        "cm": ["Using the adjective 'efficient' to modify a verb"],
        "fu": ["What is the noun form of efficient? (Efficiency)."],
        "tags": ["aptitude", "verbal-ability", "parts-of-speech"]
    },
    {
        "n": 124, "sub": "Verbal Ability - Sentence Completion", "d": "Beginner",
        "q": "Complete the sentence with an appropriate conjunction: 'He studied hard ___ he could pass the exam.'",
        "ans": "The clause expresses purpose ('why did he study hard?'). The conjunction of purpose is 'so that' (or 'in order that').\nAnswer: so that ('He studied hard so that he could pass the exam.').",
        "kp": ["Conjunction of purpose: 'so that'"],
        "cm": ["Using 'because' (which indicates cause, not intended future purpose)"],
        "fu": ["Use 'lest' in a sentence expressing negative purpose (He ran fast lest he should miss the train)."],
        "tags": ["aptitude", "verbal-ability", "conjunctions"]
    },
    {
        "n": 125, "sub": "Verbal Ability - Sentence Completion", "d": "Beginner",
        "q": "Complete the sentence with an appropriate conjunction: 'She is intelligent ___ hardworking.'",
        "ans": "Both adjectives ('intelligent' and 'hardworking') are complementary positive attributes. Use the coordinating conjunction 'and' (or 'as well as').\nAnswer: and ('She is intelligent and hardworking.').",
        "kp": ["Coordinating conjunction 'and' joins parallel positive qualities"],
        "cm": ["Using 'but' which is used for contrast"],
        "fu": ["When would you use 'but'? (e.g., 'She is intelligent but lazy')."],
        "tags": ["aptitude", "verbal-ability", "conjunctions"]
    },

    # --- Para Jumble Logic ---
    {
        "n": 126, "sub": "Verbal Ability - Para Jumbles", "d": "Intermediate",
        "q": "Arrange the sentences in logical chronological sequence:\nA. Finally, he reached the station.\nB. He left home early.\nC. He boarded the train.\nD. He walked to the station.",
        "ans": "Chronological Analysis:\n1) Action begins: B. 'He left home early.' (Opening statement)\n2) Intermediate action: D. 'He walked to the station.'\n3) Conclusion of walking: A. 'Finally, he reached the station.'\n4) Final boarding: C. 'He boarded the train.'\nLogical Order: B - D - A - C.",
        "kp": ["Chronological sequence: Leaving home -> Walking -> Reaching station -> Boarding train", "B-D-A-C"],
        "cm": ["Placing C (boarding train) before A (reaching station)"],
        "fu": ["What transition word signals that A comes toward the end? ('Finally')."],
        "tags": ["aptitude", "verbal-ability", "para-jumbles", "top-30"]
    },
    {
        "n": 127, "sub": "Verbal Ability - Para Jumbles", "d": "Intermediate",
        "q": "Arrange the sentences in logical cause-and-effect sequence:\nA. It started raining.\nB. We decided to stay indoors.\nC. We were playing cricket.\nD. The match was cancelled.",
        "ans": "Cause and Effect Analysis:\n1) Initial activity: C. 'We were playing cricket.'\n2) Disruption: A. 'It started raining.'\n3) Direct consequence on match: D. 'The match was cancelled.'\n4) Final decision: B. 'We decided to stay indoors.'\nLogical Order: C - A - D - B.",
        "kp": ["Event sequence: Playing -> Rain starts -> Match cancelled -> Stay indoors", "C-A-D-B"],
        "cm": ["Placing indoor decision before the match cancellation"],
        "fu": ["Why is C the only possible introductory sentence?"],
        "tags": ["aptitude", "verbal-ability", "para-jumbles"]
    },
    {
        "n": 128, "sub": "Verbal Ability - Para Jumbles", "d": "Intermediate",
        "q": "Arrange the sentences in logical discursive sequence:\nA. Therefore, exercise is important.\nB. Regular exercise improves health.\nC. It also reduces stress.\nD. It helps maintain fitness.",
        "ans": "Discursive Structure:\n1) Topic sentence / Thesis: B. 'Regular exercise improves health.'\n2) Supporting point 1: D. 'It helps maintain fitness.'\n3) Supporting point 2 (additive marker 'also'): C. 'It also reduces stress.'\n4) Concluding summary (marker 'Therefore'): A. 'Therefore, exercise is important.'\nLogical Order: B - D - C - A.",
        "kp": ["Thesis statement (B) -> Elaboration (D) -> Additional benefit with 'also' (C) -> Conclusion with 'Therefore' (A)", "B-D-C-A"],
        "cm": ["Placing the concluding sentence A at the beginning"],
        "fu": ["What keywords indicate a concluding sentence? ('Therefore', 'Thus', 'Hence', 'In conclusion')."],
        "tags": ["aptitude", "verbal-ability", "para-jumbles", "top-30"]
    },

    # --- Reading Comprehension Strategy ---
    {
        "n": 129, "sub": "Verbal Ability - Reading Comprehension", "d": "Beginner",
        "q": "When a Reading Comprehension question asks for the 'Main Idea' of a passage, what should you look for?",
        "ans": "Main Idea Strategy:\n1) Identify the Central Message / Core Argument that the author defends throughout the ENTIRE passage.\n2) Avoid Narrow Details: Do not select an option that summarizes only a single paragraph, supporting example, or isolated statistic.\n3) Avoid Overly Broad Generalities: Do not pick an option that extends far beyond the scope of the author's discussion.\n4) Golden Rule: The correct main idea must be broad enough to encompass all paragraphs, yet specific enough to capture the author's primary conclusion.",
        "kp": ["The central thesis of the entire passage, not an isolated detail", "Usually found in the first and concluding paragraphs", "Avoid choices that are too narrow or too broad"],
        "cm": ["Selecting a true fact from paragraph 2 that is merely a supporting example rather than the main theme"],
        "fu": ["What is the difference between the 'Title' of a passage and the 'Main Idea'?"],
        "tags": ["aptitude", "verbal-ability", "reading-comprehension", "top-30"]
    },
    {
        "n": 130, "sub": "Verbal Ability - Reading Comprehension", "d": "Beginner",
        "q": "If an answer to a Reading Comprehension question is not directly stated in the text but logically follows from the premises, what question type is it and what is the golden rule?",
        "ans": "Question Type: Inference Question (e.g., 'What can be inferred from the passage?', 'The author implies that...').\n\nGolden Rule for RC in Placement Tests:\n1) Zero Outside Knowledge: Answer strictly based on what is stated or logically necessary from the passage. Even if a statement is factually true in real life, if the passage does not support it, it is wrong.\n2) Logical Implication: An inference is an unstated fact that MUST be true if the author's stated statements are true.\n3) Beware of Extreme Words: Eliminate options with absolute qualifiers ('always', 'never', 'all', 'completely') unless explicitly backed by the passage.",
        "kp": ["Inference = logical consequence of stated facts", "NEVER use outside personal knowledge", "Avoid extreme qualifiers (always, never, impossible)"],
        "cm": ["Selecting options based on real-world general knowledge not supported in the text"],
        "fu": ["How do you differentiate between an explicit factual question and an inference question?"],
        "tags": ["aptitude", "verbal-ability", "reading-comprehension", "inference", "top-30"]
    },

    # -------------------------------------------------------------
    # SECTION D: DATA INTERPRETATION (Q131 - Q150)
    # Reference Table:
    # Year | Product A | Product B | Product C
    # 2023 | 100       | 150       | 200
    # 2024 | 120       | 180       | 240
    # 2025 | 150       | 210       | 300
    # -------------------------------------------------------------
    {
        "n": 131, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023: A=100, B=150, C=200; 2024: A=120, B=180, C=240; 2025: A=150, B=210, C=300]. What were the total sales of Product A in 2023?",
        "ans": "Read directly from row 2023, column Product A:\nSales = 100 units.",
        "kp": ["Direct table lookup: Row 2023, Col A = 100"],
        "cm": ["Reading wrong column or year"],
        "fu": ["What were sales of Product A in 2024? (120)."],
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    {
        "n": 132, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023: A=100, B=150, C=200; 2024: A=120, B=180, C=240; 2025: A=150, B=210, C=300]. What were the total sales of Product B in 2024?",
        "ans": "Read directly from row 2024, column Product B:\nSales = 180 units.",
        "kp": ["Direct table lookup: Row 2024, Col B = 180"],
        "cm": ["Reading row 2023 instead of 2024"],
        "fu": ["What were sales of Product B in 2025? (210)."],
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    {
        "n": 133, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023: A=100, B=150, C=200; 2024: A=120, B=180, C=240; 2025: A=150, B=210, C=300]. What were the total sales of Product C in 2025?",
        "ans": "Read directly from row 2025, column Product C:\nSales = 300 units.",
        "kp": ["Direct table lookup: Row 2025, Col C = 300"],
        "cm": ["Reading product B"],
        "fu": ["What were sales of Product C in 2023? (200)."],
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    {
        "n": 134, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023: A=100, B=150, C=200; 2024: A=120, B=180, C=240; 2025: A=150, B=210, C=300]. What were the total sales of all three products combined in 2023?",
        "ans": "Sum across row 2023:\nTotal Sales (2023) = Product A + Product B + Product C\n= 100 + 150 + 200 = 450 units.",
        "kp": ["100 + 150 + 200 = 450 units"],
        "cm": ["Adding across columns instead of rows"],
        "fu": ["What percentage of 2023 sales came from Product A? (100/450 = 22.22%)."],
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    {
        "n": 135, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023: A=100, B=150, C=200; 2024: A=120, B=180, C=240; 2025: A=150, B=210, C=300]. What were the total sales of all three products combined in 2025?",
        "ans": "Sum across row 2025:\nTotal Sales (2025) = Product A + Product B + Product C\n= 150 + 210 + 300 = 660 units.",
        "kp": ["150 + 210 + 300 = 660 units"],
        "cm": ["Addition mistake"],
        "fu": ["What was the total sales of all products in 2024? (120+180+240 = 540)."],
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    {
        "n": 136, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023 Total = 450; 2025 Total = 660]. What was the absolute increase in total sales from 2023 to 2025?",
        "ans": "Absolute Increase = Total(2025) - Total(2023)\n= 660 - 450 = 210 units.",
        "kp": ["Absolute change = Final - Initial = 660 - 450 = 210"],
        "cm": ["Calculating percentage instead of absolute difference"],
        "fu": ["What was the increase from 2023 to 2024? (540 - 450 = 90)."],
        "tags": ["aptitude", "data-interpretation", "tables"]
    },
    {
        "n": 137, "sub": "Data Interpretation - Tables", "d": "Intermediate",
        "q": "Table Data: [2023 Total = 450; 2025 Total = 660]. Find the percentage increase in total sales from 2023 to 2025.",
        "ans": "Formula: Percentage Increase = (Increase / Initial Value) * 100\nIncrease = 660 - 450 = 210\nInitial Value (2023) = 450\nPercentage Increase = (210 / 450) * 100 = (21 / 45) * 100 = (7 / 15) * 100 = 46.67%.",
        "kp": ["Percentage increase = (210 / 450) * 100 = 46.67%"],
        "cm": ["Dividing by 660 instead of 450"],
        "fu": ["What was the percentage increase from 2023 to 2024? (90/450 = 20%)."],
        "tags": ["aptitude", "data-interpretation", "tables", "percentage-increase", "top-30"]
    },
    {
        "n": 138, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2023: A=100, B=150, C=200]. What is the ratio of sales of Product A to Product B in 2023?",
        "ans": "Ratio = Sales(A) : Sales(B)\n= 100 : 150\nDivide by 50:\n= 2 : 3.",
        "kp": ["100 : 150 simplifies to 2 : 3"],
        "cm": ["Leaving ratio unsimplified (100:150)"],
        "fu": ["What is the ratio of Product B to Product C in 2023? (150:200 = 3:4)."],
        "tags": ["aptitude", "data-interpretation", "ratios"]
    },
    {
        "n": 139, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product C: 2023=200, 2025=300]. What is the ratio of sales of Product C in 2023 to Product C in 2025?",
        "ans": "Ratio = Sales(C, 2023) : Sales(C, 2025)\n= 200 : 300\nDivide by 100:\n= 2 : 3.",
        "kp": ["200 : 300 simplifies to 2 : 3"],
        "cm": ["Inverting the years"],
        "fu": ["What is the ratio of A in 2023 to A in 2025? (100:150 = 2:3)."],
        "tags": ["aptitude", "data-interpretation", "ratios"]
    },
    {
        "n": 140, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product A: 2023=100, 2024=120, 2025=150]. What was the average annual sales of Product A over the 3 years?",
        "ans": "Sum of sales for A = 100 + 120 + 150 = 370 units.\nNumber of years = 3.\nAverage = 370 / 3 = 123.33 units.",
        "kp": ["Average = 370 / 3 = 123.33"],
        "cm": ["Dividing by 2 instead of 3"],
        "fu": ["In which year was sales above average? (2025 with 150)."],
        "tags": ["aptitude", "data-interpretation", "averages"]
    },
    {
        "n": 141, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product B: 2023=150, 2024=180, 2025=210]. What was the average annual sales of Product B over the 3 years?",
        "ans": "Sum of sales for B = 150 + 180 + 210 = 540 units.\nNumber of years = 3.\nAverage = 540 / 3 = 180 units.\n(Notice that 150, 180, 210 form an AP, so middle term is average = 180).",
        "kp": ["Sum = 540; Average = 540 / 3 = 180"],
        "cm": ["Arithmetic error"],
        "fu": ["Did Product B have steady linear growth? (Yes, +30 each year)."],
        "tags": ["aptitude", "data-interpretation", "averages"]
    },
    {
        "n": 142, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product C: 2023=200, 2024=240, 2025=300]. What was the average annual sales of Product C over the 3 years?",
        "ans": "Sum of sales for C = 200 + 240 + 300 = 740 units.\nNumber of years = 3.\nAverage = 740 / 3 = 246.67 units.",
        "kp": ["Average = 740 / 3 = 246.67"],
        "cm": ["Rounding prematurely"],
        "fu": ["Which product had the highest single-year sales? (Product C in 2025 = 300)."],
        "tags": ["aptitude", "data-interpretation", "averages"]
    },
    {
        "n": 143, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [3-Year Totals: A=370, B=540, C=740]. Which product had the highest total sales over the 3 years?",
        "ans": "Compare 3-year total sales:\nProduct A = 100 + 120 + 150 = 370\nProduct B = 150 + 180 + 210 = 540\nProduct C = 200 + 240 + 300 = 740\nProduct C has the highest total sales (740 units).\nAnswer: Product C.",
        "kp": ["Product C = 740 units is the highest"],
        "cm": ["Picking Product B"],
        "fu": ["Which product had the lowest total sales? (Product A = 370)."],
        "tags": ["aptitude", "data-interpretation", "comparison"]
    },
    {
        "n": 144, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product A: 2023=100, 2024=120, 2025=150]. What is the total 3-year cumulative sales of Product A?",
        "ans": "Sum = 100 + 120 + 150 = 370 units.",
        "kp": ["Total sales of A = 370"],
        "cm": ["Addition slip"],
        "fu": ["What percentage of A's 3-year sales occurred in 2025? (150/370 = 40.54%)."],
        "tags": ["aptitude", "data-interpretation", "totals"]
    },
    {
        "n": 145, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product B: 2023=150, 2024=180, 2025=210]. What is the total 3-year cumulative sales of Product B?",
        "ans": "Sum = 150 + 180 + 210 = 540 units.",
        "kp": ["Total sales of B = 540"],
        "cm": ["Addition slip"],
        "fu": ["What is 540 / 3? (180)."],
        "tags": ["aptitude", "data-interpretation", "totals"]
    },
    {
        "n": 146, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product C: 2023=200, 2024=240, 2025=300]. What is the total 3-year cumulative sales of Product C?",
        "ans": "Sum = 200 + 240 + 300 = 740 units.",
        "kp": ["Total sales of C = 740"],
        "cm": ["Addition slip"],
        "fu": ["Compare C's total with A's total."],
        "tags": ["aptitude", "data-interpretation", "totals"]
    },
    {
        "n": 147, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product C total = 740, Product A total = 370]. Find the difference between the total 3-year sales of Product C and Product A.",
        "ans": "Difference = Total(C) - Total(A)\n= 740 - 370 = 370 units.\n(Notice that Product C sold exactly double of Product A: 740 = 2 * 370).",
        "kp": ["Difference = 740 - 370 = 370 units", "C is exactly 2x of A"],
        "cm": ["Subtracting wrong product values"],
        "fu": ["Product C's sales are what percent of Product A's sales? (200%)."],
        "tags": ["aptitude", "data-interpretation", "difference"]
    },
    {
        "n": 148, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product A: 2023=100, 2025=150]. What was the percentage increase in Product A sales from 2023 to 2025?",
        "ans": "Increase = 150 - 100 = 50 units.\nBase value (2023) = 100.\nPercentage Increase = (50 / 100) * 100 = 50%.\nAnswer: 50%.",
        "kp": ["Percentage increase = (50 / 100) * 100 = 50%"],
        "cm": ["Dividing by 150"],
        "fu": ["What was the increase from 2023 to 2024? (20%)."],
        "tags": ["aptitude", "data-interpretation", "percentage-increase"]
    },
    {
        "n": 149, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [Product C: 2023=200, 2025=300]. What was the percentage increase in Product C sales from 2023 to 2025?",
        "ans": "Increase = 300 - 200 = 100 units.\nBase value (2023) = 200.\nPercentage Increase = (100 / 200) * 100 = 50%.\nAnswer: 50%.\n(Note: Both Product A and Product C grew by the exact same rate of 50% from 2023 to 2025).",
        "kp": ["Percentage increase = (100 / 200) * 100 = 50%", "Identical growth rate as Product A"],
        "cm": ["Dividing by 300"],
        "fu": ["What was Product B's growth rate? (210 - 150) / 150 = 60 / 150 = 40%."],
        "tags": ["aptitude", "data-interpretation", "percentage-increase"]
    },
    {
        "n": 150, "sub": "Data Interpretation - Tables", "d": "Beginner",
        "q": "Table Data: [2024: A=120, B=180, C=240]. What were the combined sales of Product A and Product B in 2024?",
        "ans": "Combined Sales = Sales(A, 2024) + Sales(B, 2024)\n= 120 + 180 = 300 units.\nAnswer: 300 units.",
        "kp": ["120 + 180 = 300 units"],
        "cm": ["Including Product C in calculation"],
        "fu": ["Was combined A+B in 2024 greater than Product C in 2024? (Yes, 300 > 240)."],
        "tags": ["aptitude", "data-interpretation", "tables", "top-30"]
    }
]


def run():
    with SessionLocal() as db:
        existing_rows = db.scalars(select(Question)).all()
        hash_to_question = {row.question_hash: row for row in existing_rows}
        id_to_question = {row.id: row for row in existing_rows}

        created = 0
        updated = 0

        for item in RAW_QUESTIONS:
            idx = item["n"]
            q_id = f"apt-{idx:03d}"
            q_text = item["q"]
            h = question_fingerprint(q_text)
            tags = list(item.get("tags", []))
            tags.append("aptitude")
            if "top-30" not in tags and idx in [5, 9, 13, 15, 21, 27, 32, 34, 41, 44, 47, 48, 51, 52, 60, 63, 65, 68, 74, 76, 81, 83, 84, 97, 98, 102, 104, 113, 114, 117, 119, 120, 122, 126, 128, 129, 130, 137, 150]:
                tags.append("top-30")

            sub = item["sub"]
            d = item["d"]
            ans = item["ans"]
            kp = item["kp"]
            cm = item["cm"]
            fu = item["fu"]
            crit = ["Mathematical and logical correctness", "Application of standard shortcut formulas", "Accurate handling of edge-cases and units"]

            if h in hash_to_question:
                row = hash_to_question[h]
                merged_tags = list(dict.fromkeys(list(row.tags or []) + tags))
                row.tags = merged_tags
                row.reference_answer = ans
                row.key_points = kp
                row.common_mistakes = cm
                row.follow_up_questions = fu
                row.subcategory = sub
                row.difficulty = d
                row.category = "Aptitude"
                row.question_type = "technical"
                updated += 1
                log.info(f"Updated: {row.id} - {q_text[:40]}")
            elif q_id in id_to_question:
                row = id_to_question[q_id]
                row.question = q_text
                row.question_hash = h
                row.category = "Aptitude"
                row.subcategory = sub
                row.difficulty = d
                row.reference_answer = ans
                row.key_points = kp
                row.common_mistakes = cm
                row.follow_up_questions = fu
                row.tags = list(dict.fromkeys(list(row.tags or []) + tags))
                updated += 1
                log.info(f"Updated ID: {q_id} - {q_text[:40]}")
            else:
                new_row = Question(
                    id=q_id,
                    question=q_text,
                    question_hash=h,
                    category="Aptitude",
                    subcategory=sub,
                    difficulty=d,
                    question_type="technical",
                    target_roles=ROLES,
                    interview_stage=STAGES,
                    reference_answer=ans,
                    key_points=kp,
                    evaluation_criteria=crit,
                    common_mistakes=cm,
                    follow_up_questions=fu,
                    tags=tags,
                    is_active=True,
                )
                db.add(new_row)
                id_to_question[q_id] = new_row
                hash_to_question[h] = new_row
                created += 1
                log.info(f"Created: {q_id} - {q_text[:40]}")

        db.commit()
        print(f"Seeding Aptitude 150 Completed! Created: {created}, Updated: {updated}")


if __name__ == "__main__":
    run()
