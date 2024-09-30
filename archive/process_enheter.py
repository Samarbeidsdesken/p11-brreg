import pandas as pd

# Load the CSV file

df = pd.read_csv('enheter/alle_enheter_110924', delimiter=',')

# Replace empty strings in date columns with NaN (equivalent to NULL)
date_columns = ['registreringsdatoenhetsregisteret', 'stiftelsesdato', 'konkursdato',
                'underAvviklingDato', 'tvangsopplostPgaManglendeDagligLederDato',
                'tvangsopplostPgaManglendeRevisorDato', 'tvangsopplostPgaManglendeRegnskapDato',
                'tvangsopplostPgaMangelfulltStyreDato', 'tvangsavvikletPgaManglendeSlettingDato',
                'vedtektsdato']

# Replace empty date values with NaN
df[date_columns] = df[date_columns].replace("", pd.NA)

pd.options.display.float_format = '{:,.0f}'.format


# Save the cleaned CSV
df.to_csv('enheter/alle_enheter_110924.csv', index=False)
