import pathlib
import pandas as pd

path = pathlib.Path('.')
cols = ['id_', 'title', 'acceptance', 'difficulty', 'frequency', 'link']
data = pd.DataFrame(columns=cols)
mapping = {}
difficulty_level_mapping = {
    'Easy': 1,
    'Medium': 2,
    'Hard': 3
}
for file in path.glob('*.csv'):
    df = pd.read_csv(file.name, names=cols)
    for index, row in df.iterrows():
        try:
            mapping[row['id_']] = [row['title'], difficulty_level_mapping[row['difficulty']], row['acceptance'], row['link']]
        except KeyError:
            print(row)
    data = pd.concat([data, df], ignore_index=True)
sorted_data = data.groupby(by='id_').count().sort_values(by=['title', 'id_'], ascending=[False, True])

sorted_complete_data = pd.DataFrame(columns=cols)
for id_, row in sorted_data.iterrows():
    try:
        title = mapping[id_][0]
    except KeyError:
        continue
    difficulty = mapping[id_][1]
    acceptance = mapping[id_][2]
    link = mapping[id_][3]
    entry = pd.DataFrame.from_dict({
        'id_': [id_],
        'title': [title],
        'frequency': [row['frequency']],
        'difficulty': [difficulty],
        'acceptance': [acceptance],
        'link': [link]
    })
    sorted_complete_data = pd.concat([sorted_complete_data, entry], ignore_index=True)

sorted_complete_data.sort_values(
    by=['frequency', 'difficulty', 'acceptance', 'id_', 'title'],
    ascending=[False, True, True, True, True]
)
sorted_complete_data['difficulty'] = sorted_complete_data['difficulty'].apply(
    lambda d: 'Easy' if d < 2 else 'Hard' if d > 2 else 'Medium'
)
sorted_complete_data.to_excel('listOfQuestionsSortedByFrequency.xlsx')
