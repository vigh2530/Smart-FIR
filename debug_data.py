import pandas as pd

df = pd.read_csv('data/FIR_DATASET.csv')
df['IPC'] = df['URL'].str.extract(r'section-(\d+)')

ipc_counts = df['IPC'].value_counts()
valid_ipcs = ipc_counts[ipc_counts >= 5].index

print(f'Total rows: {len(df)}')
print(f'Valid IPCs: {len(valid_ipcs)}')
print(f'After filter: {len(df[df["IPC"].isin(valid_ipcs)])}')
print(f'IPC counts distribution:\n{ipc_counts.head(20)}')
