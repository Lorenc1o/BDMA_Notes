*SENSE:Maximize
NAME          Visit_the_maximum_number_of_sites_in_12_hours_with_a_budget_of_65€
ROWS
 N  Number_of_sites_to_visit;_to_be_maximized
 L  Time_constraint
 L  Budget_constraint
COLUMNS
    MARK      'MARKER'                 'INTORG'
    AC:_x12   Time_constraint   1.500000000000e+00
    AC:_x12   Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    AT:_x2    Time_constraint   1.000000000000e+00
    AT:_x2    Budget_constraint   9.500000000000e+00
    AT:_x2    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    BS:_x8    Time_constraint   2.000000000000e+00
    BS:_x8    Budget_constraint   8.000000000000e+00
    BS:_x8    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    CA:_x5    Time_constraint   2.000000000000e+00
    CA:_x5    Budget_constraint   1.000000000000e+01
    CA:_x5    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    CN:_x7    Time_constraint   2.000000000000e+00
    CN:_x7    Budget_constraint   5.000000000000e+00
    CN:_x7    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    CP:_x6    Time_constraint   2.500000000000e+00
    CP:_x6    Budget_constraint   1.000000000000e+01
    CP:_x6    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    JT:_x4    Time_constraint   1.500000000000e+00
    JT:_x4    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    ML:_x1    Time_constraint   3.000000000000e+00
    ML:_x1    Budget_constraint   1.200000000000e+01
    ML:_x1    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    MO:_x3    Time_constraint   2.000000000000e+00
    MO:_x3    Budget_constraint   1.100000000000e+01
    MO:_x3    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    PC:_x10   Time_constraint   7.500000000000e-01
    PC:_x10   Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    SC:_x9    Time_constraint   1.500000000000e+00
    SC:_x9    Budget_constraint   8.500000000000e+00
    SC:_x9    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    TE:_x0    Time_constraint   4.500000000000e+00
    TE:_x0    Budget_constraint   1.550000000000e+01
    TE:_x0    Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    TM:_x11   Time_constraint   2.000000000000e+00
    TM:_x11   Budget_constraint   1.500000000000e+01
    TM:_x11   Number_of_sites_to_visit;_to_be_maximized   1.000000000000e+00
    MARK      'MARKER'                 'INTEND'
RHS
    RHS       Time_constraint   1.200000000000e+01
    RHS       Budget_constraint   6.500000000000e+01
BOUNDS
 BV BND       AC:_x12 
 BV BND       AT:_x2  
 BV BND       BS:_x8  
 BV BND       CA:_x5  
 BV BND       CN:_x7  
 BV BND       CP:_x6  
 BV BND       JT:_x4  
 BV BND       ML:_x1  
 BV BND       MO:_x3  
 BV BND       PC:_x10 
 BV BND       SC:_x9  
 BV BND       TE:_x0  
 BV BND       TM:_x11 
ENDATA
