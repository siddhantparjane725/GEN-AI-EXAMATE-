# MatdarMitra Evaluation Results

Metric: percentage of answerable questions where at least one expected source PDF appears in the retrieved results.

| Configuration | Chunk size (words) | Top K | Source hits | Hit rate | Q6 abstention |
|---|---:|---:|---:|---:|---|
| Config A | 800 | 3 | 14/14 | 100.00% | PASS |
| Config B | 800 | 5 | 14/14 | 100.00% | PASS |

## Winner: Config A

The winner has the highest source hit rate. Ties are resolved in favour of the smaller top_k.

## Question-level Results

### Config A

- **Q1 – PASS:** What documents are needed with Form 6?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, 6b.pdf
- **Q2 – PASS:** Which form is used to correct a spelling mistake in my name on the electoral roll?
  - Expected: 8.pdf
  - Retrieved: 8.pdf, Final-ER-FAQ.pdf
- **Q3 – PASS:** Who can object to the inclusion of a person's name in the voter list?
  - Expected: 7.pdf
  - Retrieved: 7.pdf, Final-ER-FAQ.pdf
- **Q4 – PASS:** What documents can be used as proof of age for new voter registration?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, Final-ER-FAQ.pdf
- **Q5 – PASS:** How can the name of a deceased person be removed from the electoral roll?
  - Expected: 7.pdf
  - Retrieved: 7.pdf, Final-ER-FAQ.pdf
- **Q6 – PASS:** Who is the BLO for ward 5 in Kopargaon?
  - Expected: I don't know
  - Retrieved: No source required
- **Q7 – PASS:** How can an Indian citizen living abroad register as a voter?
  - Expected: 6a.pdf
  - Retrieved: 6a.pdf, Final-ER-FAQ.pdf
- **Q8 – PASS:** Is Aadhaar mandatory for voter registration?
  - Expected: 6.pdf, 6b.pdf
  - Retrieved: 6b.pdf, Final-ER-FAQ.pdf
- **Q9 – PASS:** Which form should I use after shifting my residence?
  - Expected: 8.pdf
  - Retrieved: 6a.pdf, 7.pdf, 8.pdf
- **Q10 – PASS:** Can I submit my voter registration application online?
  - Expected: Final-ER-FAQ.pdf
  - Retrieved: 6.pdf, Final-ER-FAQ.pdf
- **Q11 – PASS:** Which form is used to change personal details in the electoral roll?
  - Expected: 8.pdf
  - Retrieved: 7.pdf, 8.pdf
- **Q12 – PASS:** Which form is used to object to an incorrect entry in the electoral roll?
  - Expected: 7.pdf
  - Retrieved: 7.pdf, Final-ER-FAQ.pdf
- **Q13 – PASS:** What proof of residence can be attached with Form 6?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, Final-ER-FAQ.pdf
- **Q14 – PASS:** What is Form 6B used for?
  - Expected: 6b.pdf
  - Retrieved: 6a.pdf, 6b.pdf
- **Q15 – PASS:** What should an applicant do if none of the listed age proof documents is available?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, Final-ER-FAQ.pdf

### Config B

- **Q1 – PASS:** What documents are needed with Form 6?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, 6a.pdf, 6b.pdf
- **Q2 – PASS:** Which form is used to correct a spelling mistake in my name on the electoral roll?
  - Expected: 8.pdf
  - Retrieved: 7.pdf, 8.pdf, Final-ER-FAQ.pdf
- **Q3 – PASS:** Who can object to the inclusion of a person's name in the voter list?
  - Expected: 7.pdf
  - Retrieved: 7.pdf, Final-ER-FAQ.pdf
- **Q4 – PASS:** What documents can be used as proof of age for new voter registration?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, Final-ER-FAQ.pdf
- **Q5 – PASS:** How can the name of a deceased person be removed from the electoral roll?
  - Expected: 7.pdf
  - Retrieved: 7.pdf, Final-ER-FAQ.pdf
- **Q6 – PASS:** Who is the BLO for ward 5 in Kopargaon?
  - Expected: I don't know
  - Retrieved: No source required
- **Q7 – PASS:** How can an Indian citizen living abroad register as a voter?
  - Expected: 6a.pdf
  - Retrieved: 6a.pdf, Final-ER-FAQ.pdf
- **Q8 – PASS:** Is Aadhaar mandatory for voter registration?
  - Expected: 6.pdf, 6b.pdf
  - Retrieved: 6.pdf, 6b.pdf, Final-ER-FAQ.pdf
- **Q9 – PASS:** Which form should I use after shifting my residence?
  - Expected: 8.pdf
  - Retrieved: 6a.pdf, 7.pdf, 8.pdf, Final-ER-FAQ.pdf
- **Q10 – PASS:** Can I submit my voter registration application online?
  - Expected: Final-ER-FAQ.pdf
  - Retrieved: 6.pdf, Final-ER-FAQ.pdf
- **Q11 – PASS:** Which form is used to change personal details in the electoral roll?
  - Expected: 8.pdf
  - Retrieved: 7.pdf, 8.pdf, Final-ER-FAQ.pdf
- **Q12 – PASS:** Which form is used to object to an incorrect entry in the electoral roll?
  - Expected: 7.pdf
  - Retrieved: 7.pdf, 8.pdf, Final-ER-FAQ.pdf
- **Q13 – PASS:** What proof of residence can be attached with Form 6?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, 6a.pdf, Final-ER-FAQ.pdf
- **Q14 – PASS:** What is Form 6B used for?
  - Expected: 6b.pdf
  - Retrieved: 6.pdf, 6a.pdf, 6b.pdf
- **Q15 – PASS:** What should an applicant do if none of the listed age proof documents is available?
  - Expected: 6.pdf
  - Retrieved: 6.pdf, 8.pdf, Final-ER-FAQ.pdf