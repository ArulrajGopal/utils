# MSSQL DDL Creator

Generates a Microsoft SQL Server `DROP TABLE` / `CREATE TABLE` / `INSERT INTO` script from a delimited text file. Column types (`int`, `decimal`, `date`, `varchar`) and `varchar` lengths are inferred automatically from the data.

## Requirements

- Python 3
- No third-party packages required

## Files

- [source.py](source.py) — the script
- [Reference/SampleInput.txt](Reference/SampleInput.txt) — example input
- [Reference/created_output.txt](Reference/created_output.txt) — example output generated from the sample input

## Usage

```
python source.py <input_file> <table_name> <separator> > <output_file>
```

| Argument | Description |
|---|---|
| `input_file` | Path to the delimited text file to convert |
| `table_name` | Name to use for the generated SQL table |
| `separator` | Character(s) that separate columns in the input file (e.g. `,`) |
| `output_file` | The script prints the generated SQL to stdout, so redirect it (`>`) to save it to a file |

### Example

```
python source.py Reference/SampleInput.txt mytable "," > created_output.txt
```

Input ([Reference/SampleInput.txt](Reference/SampleInput.txt)):

```
Id, name, age
1, Arul, 45
2, Vignesh, 73
3, Sekar,34
1, Arul, 45
2,Vignesh,24
4, Vivek,56
5, Ramu,67
```

Output ([Reference/created_output.txt](Reference/created_output.txt)):

```sql
drop table if exists mytable;

create table mytable(
Id int ,
 name varchar(16) ,
 age int
);

insert into mytable
values
('1', ' Arul', ' 45') ,
('2', ' Vignesh', ' 73') ,
('3', ' Sekar', '34') ,
('1', ' Arul', ' 45') ,
('2', 'Vignesh', '24') ,
('4', ' Vivek', '56') ,
('5', ' Ramu', '67') ;

select * from mytable
```

## Input file format

- The first line must contain the column names, separated by `separator`.
- Every following line is a data row, values separated by the same `separator`.
- Any whitespace around values (e.g. after a `,`) is kept as-is in the output, so keep the separator consistent throughout the file.

## Type inference

For each column, the type is decided from the **first data row only**, in this order:

1. `int` — if the value parses as an integer
2. `decimal(n,2)` — if the value parses as a float
3. `date` — if the value parses as `YYYY-MM-DD`
4. `varchar(n)` — otherwise, where `n` is twice the longest value found in that column across all rows

## Limitations

- Type inference only looks at the first row of data per column — if later rows don't match that type (e.g. a numeric column that later contains text), the generated `CREATE TABLE` types won't be accurate for those rows.
- All values in the generated `INSERT` statement are wrapped in quotes regardless of inferred type, so the insert itself will still run even if a column's declared type doesn't perfectly match every value.
- Designed for small/medium files — the whole file is loaded into memory.
