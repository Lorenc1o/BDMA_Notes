import openpyxl

def create_voting_profiles():
    # Create a new workbook
    wb = openpyxl.Workbook()
    # Select the active worksheet
    ws = wb.active
    # Define the voting profiles
    profiles = [
        [5, ['a', 'b', 'c', 'd']],
        [4, ['a', 'c', 'b', 'd']],
        [2, ['d', 'b', 'a', 'c']],
        [6, ['d', 'b', 'c', 'a']],
        [8, ['c', 'b', 'a', 'd']],
        [2, ['d', 'c', 'b', 'a']]
    ]
    # Write the voting profiles to the worksheet
    for profile in profiles:
        for _ in range(profile[0]):
            ws.append(profile[1])
    # Save the workbook, overwriting the previous file
    wb.save('data.xlsx')

def read_voting_profiles():
    # Open the workbook
    wb = openpyxl.load_workbook('data.xlsx')
    # Select the active worksheet
    ws = wb.active
    # Read the voting profiles
    profiles = {}
    for row in ws.iter_rows(min_row=1, max_col=4):
        profile = ''
        for cell in row:
            profile += cell.value
        
        if profile not in profiles.keys():
            profiles[profile] = 1
        else:
            profiles[profile] += 1
    
    return profiles

if __name__ == '__main__':
    create_voting_profiles()
    profiles = read_voting_profiles()
    print(profiles)

