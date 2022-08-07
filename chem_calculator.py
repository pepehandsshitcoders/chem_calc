import re
from enum import Enum
from PyQt5 import QtCore, QtWidgets, uic
import sys

def mol_split(a):
    m = re.search(r"\((.+)\)", a)
    ms = None
    am = []
    if m: # если есть скобки
        am = a.split('(') # то делим ввод на часть до ( и после
        al = re.split('([A-Z][a-z]|[A-Z])', am[0]) # ввод до ( делим по элементам и числам (Al, 23, O, Na, 5, H)
    else: # если скобок нет
        al = re.split('([A-Z][a-z]|[A-Z])', a) # то весь ввод делим по элементам и числам

    al = list(filter(None, al)) # убираем из al пустые элементы

    for i in range(len(al)): # проходим по всем элементам al
        if al[i].isdigit(): # и если элемент - число
            al[i] = int(al[i]) # делаем его интом

    al2d = []
    curlist = []
    for i in al: # проходим по всем элементам al
        if type(i) == str: # если элемент - строка
            curlist.append(i) # пихаем его во временный лист
            if al[-1] == i: # если элемент последний в al
                curlist.append(1) # пихаем во временный лист 1
                al2d.append(curlist) # пихаем временный лист в al2d
                curlist = [] # делаем временный лист пустым
            elif type(al[al.index(i) + 1]) == str: # если следующий элемент - строка
                curlist.append(1) # пихаем во временный лист 1
                al2d.append(curlist) # пихаем временный лист в al2d
                curlist = [] # делаем временный лист пустым
        elif type(i) == int: # если элемент - число
            curlist.append(i) # пихаем во временный лист это число
            al2d.append(curlist) # пихаем временный лист в al2d
            curlist = [] # делаем временный лист пустым

    if m: # если есть скобки
        ar = am[1].split(')') # из ***(****)** получаем список ['****', '**']
        aj = re.split('([A-Z][a-z]|[A-Z])', ar[0]) # **** делим на элементы и числа
        aj = list(filter(None, aj)) # убираем из aj пустые элементы

        for i in range(len(aj)): # проходим по всем элементам aj
            if aj[i].isdigit(): # и если элемент - число
                aj[i] = int(aj[i]) # делаем его интом

        if ar[1].isdigit(): # если ** - число
            ar[1] = int(ar[1]) # делаем его интом
        else: # если ** пустая строка
            ar[1] = 1 # делаем ** числом 1

        al12d = []
        curlist = []
        for i in aj:
            if type(i) == str:
                curlist.append(i)
                if aj[-1] == i:
                    curlist.append(ar[1])
                    al12d.append(curlist)
                    curlist = []
                elif type(aj[aj.index(i) + 1]) == str:
                    curlist.append(ar[1])
                    al12d.append(curlist)
                    curlist = []
            elif type(i) == int:
                curlist.append(i*ar[1])
                al12d.append(curlist)
                curlist = []

        al2d.extend(al12d) # добовляем к al2d al12d
        ms = ar[0] # ms - **** (то что в скобках в виде строки)
    return al2d, ms

class Subgroup(Enum):
    A = 1
    B = 2

class Element:
    def __init__(self, PP, FullName, Row, Group, Subgroup, MolMass, isMetal = 1):
        self.PP = PP
        self.FullName = FullName
        self.Row = Row
        self.Group = Group
        self.Subgroup = Subgroup
        self.MolMass = MolMass
        self.isMetal = bool(isMetal)

elements = {'H' : Element(1,   'Hydrogenium',   1,  1,  Subgroup.A, 1,  0),
            'He': Element(2,   'Helium',        1,  8,  Subgroup.A, 4,  0),
            'Li': Element(3,   'Lithium',       2,  1,  Subgroup.A, 7),
            'Be': Element(4,   'Beryllium',     2,  2,  Subgroup.A, 9),
            'B' : Element(5,   'Borum',         2,  3,  Subgroup.A, 11, 0),
            'C' : Element(6,   'Carboneum',     2,  4,  Subgroup.A, 12, 0),
            'N' : Element(7,   'Nitrogenium',   2,  5,  Subgroup.A, 14, 0),
            'O' : Element(8,   'Oxygenium',     2,  6,  Subgroup.A, 16, 0),
            'F' : Element(9,   'Fluorum',       2,  7,  Subgroup.A, 19, 0),
            'Ne': Element(10,  'Neon',          3,  8,  Subgroup.A, 20, 0),
            'Na': Element(11,  'Natrium',       3,  1,  Subgroup.A, 23),
            'Mg': Element(12,  'Magnesium',     3,  2,  Subgroup.A, 24),
            'Al': Element(13,  'Aluminium',     3,  3,  Subgroup.A, 27),
            'Si': Element(14,  'Silicium',      3,  4,  Subgroup.A, 28, 0),
            'P' : Element(15,  'Phosphorus',    3,  5,  Subgroup.A, 31, 0),
            'S' : Element(16,  'Sulfur',        3,  6,  Subgroup.A, 32, 0),
            'Cl': Element(17,  'Chlorine',      3,  7,  Subgroup.A, 35, 0),
            'Ar': Element(18,  'Argon',         3,  8,  Subgroup.A, 40, 0),
            'K' : Element(19,  'Calium',        4,  1,  Subgroup.A, 39),
            'Ca': Element(20,  'Calcium',       4,  2,  Subgroup.A, 40),
            'Sc': Element(21,  'Scandium',      4,  3,  Subgroup.B, 45),
            'Ti': Element(22,  'Titanium',      4,  4,  Subgroup.B, 48),
            'V' : Element(23,  'Vanadium',      4,  5,  Subgroup.B, 51),
            'Cr': Element(24,  'Chromium',      4,  6,  Subgroup.B, 52),
            'Mn': Element(25,  'Manganesium',   4,  7,  Subgroup.B, 55),
            'Fe': Element(26,  'Ferrum',        4,  8,  Subgroup.B, 56),
            'Co': Element(27,  'Cobaltum',      4,  8,  Subgroup.B, 59),
            'Ni': Element(28,  'Niccolum',      4,  8,  Subgroup.B, 59),
            'Cu': Element(29,  'Cuprum',        5,  1,  Subgroup.B, 64),
            'Zn': Element(30,  'Zincum',        5,  2,  Subgroup.B, 65),
            'Ga': Element(31,  'Gallium',       5,  3,  Subgroup.A, 70),
            'Ge': Element(32,  'Germanium',     5,  4,  Subgroup.A, 73),
            'As': Element(33,  'Arsenicum',     5,  5,  Subgroup.A, 75, 0),
            'Se': Element(34,  'Selenium',      5,  6,  Subgroup.A, 79, 0),
            'Br': Element(35,  'Bromum',        5,  7,  Subgroup.A, 80, 0),
            'Kr': Element(36,  'Crypton',       5,  8,  Subgroup.A, 84, 0),
            'Rb': Element(37,  'Rubidium',      6,  1,  Subgroup.A, 85),
            'Sr': Element(38,  'Strontium',     6,  2,  Subgroup.A, 88),
            'Y' : Element(39,  'Yttrium',       6,  3,  Subgroup.B, 89),
            'Zr': Element(40,  'Zirconium',     6,  4,  Subgroup.B, 91),
            'Nb': Element(41,  'Niobium',       6,  5,  Subgroup.B, 93),
            'Mo': Element(42,  'Molybdaenum',   6,  6,  Subgroup.B, 96),
            'Tc': Element(43,  'Technetium',    6,  7,  Subgroup.B, 99),
            'Ru': Element(44,  'Ruthenium',     6,  8,  Subgroup.B, 101),
            'Rh': Element(45,  'Rhodium',       6,  8,  Subgroup.B, 103),
            'Pd': Element(46,  'Palladium',     6,  8,  Subgroup.B, 106),
            'Ag': Element(47,  'Argentum',      7,  1,  Subgroup.B, 108),
            'Cd': Element(48,  'Cadmium',       7,  2,  Subgroup.B, 112),
            'In': Element(49,  'Indium',        7,  3,  Subgroup.A, 115),
            'Sn': Element(50,  'Stannum',       7,  4,  Subgroup.A, 119),
            'Sb': Element(51,  'Stibium',       7,  5,  Subgroup.A, 122),
            'Te': Element(52,  'Tellurium',     7,  6,  Subgroup.A, 128, 0),
            'I' : Element(53,  'Iodine',        7,  7,  Subgroup.A, 127, 0),
            'Xe': Element(54,  'Xenon',         7,  8,  Subgroup.A, 131, 0),
            'Cs': Element(55,  'Caesium',       8,  1,  Subgroup.A, 133),
            'Ba': Element(56,  'Barium',        8,  2,  Subgroup.A, 137),
            #***
            'Hf': Element(72,  'Hafnium',       8,  4,  Subgroup.B, 178),
            'Ta': Element(73,  'Tantalum',      8,  5,  Subgroup.B, 181),
            'W' : Element(74,  'Wolframium',    8,  6,  Subgroup.B, 184),
            'Re': Element(75,  'Rhenium',       8,  7,  Subgroup.B, 186),
            'Os': Element(76,  'Osmium',        8,  8,  Subgroup.B, 190),
            'Ir': Element(77,  'Iridium',       8,  8,  Subgroup.B, 192),
            'Pt': Element(78,  'Platinum',      8,  8,  Subgroup.B, 195),
            'Au': Element(79,  'Aurum',         9,  1,  Subgroup.B, 197),
            'Hg': Element(80,  'Hydrargyrum',   9,  2,  Subgroup.B, 201),
            'Tl': Element(81,  'Thallium',      9,  3,  Subgroup.A, 204),
            'Pb': Element(82,  'Plumbum',       9,  4,  Subgroup.A, 207),
            'Bi': Element(83,  'Bismuthum',     9,  5,  Subgroup.A, 209),
            'Po': Element(84,  'Polonium',      9,  6,  Subgroup.A, 209),
            'At': Element(85,  'Astatine',      9,  7,  Subgroup.A, 210, 0),
            'Rn': Element(86,  'Radon',         9,  8,  Subgroup.A, 222, 0),
            'Fr': Element(87,  'Francium',      10, 1,  Subgroup.A, 223),
            'Ra': Element(88,  'Radium',        10, 2,  Subgroup.A, 226),
            'Rf': Element(104, 'Rutherfordium', 10, 4,  Subgroup.B, 267),
            'Db': Element(105, 'Dubnium',       10, 5,  Subgroup.B, 268),
            'Sg': Element(106, 'Seaborgium',    10, 6,  Subgroup.B, 269),
            'Bh': Element(107, 'Bohrium',       10, 7,  Subgroup.B, 270),
            'Hs': Element(108, 'Hassium',       10, 8,  Subgroup.B, 271),
            'Mt': Element(109, 'Meitnerium',    10, 9,  Subgroup.B, 272)}

acids = ['H(F)', 'H(Cl)' ,'H(NO2)', 'H(NO3)', 'H2(S)', 'H2(SO3)', 'H2(SO4)', 'H2(CO3)', 'H2(SiO3)', 'H3(PO4)']
acid_oxides = {'N2O3': acids[2], 'N2O5': acids[3], 'SO2': acids[5], 'SO3': acids[6], 'CO2': acids[7], 'P2O5': acids[9]}
acid_residues = ['F', 'Cl', 'SO3', 'SO4', 'S', 'NO3', 'NO2', 'CO3', 'SiO3', 'PO4']
acid_oxides_2 = {'N2O3': acid_residues[6], 'N2O5': acid_residues[5], 'SO2': acid_residues[2], 'SO3': acid_residues[3], 'CO2': acid_residues[7], 'P2O5': acid_residues[9]}
Alkali_Me = ["Na", "K", "Li", "Rb", "Cs", "Fr", "Ca", "Sr", "Ba", "Ra"]

class MolTypes(Enum):
    Oxide = 1
    Acid = 2
    AcidOxide = 3
    Hydroxide = 4
    Salt = 5
    Common = 6

def lcm(a, b):
    m = a * b
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return m // (a + b)

def info(a):
    elem_pp = 0
    elem_row = 0
    elem_group = 0
    elem_subgroup = Subgroup.B
    elem_name = ''
    elem_full_name = ''
    elem_mass = 0
    elem_metal = False

    for key, value in elements.items():
        if key == a:
            elem_pp = value.PP
            elem_full_name = value.FullName
            elem_row = value.Row
            elem_group = value.Group
            elem_subgroup = value.Subgroup
            elem_name = key
            elem_mass = value.MolMass
            elem_metal = value.isMetal

    return elem_row, elem_group, elem_subgroup, elem_name, elem_full_name, elem_mass, elem_metal, elem_pp

def React_CalculationV2(molecules):
    mol1, mol1_inBrackets,  = mol_split(molecules[0])
    mol2, mol2_inBrackets = mol_split(molecules[1])

    mol1_type = MolTypes.Common
    mol2_type = MolTypes.Common

    acidResidue_val = 1
    
    elem1_val = 0
    elem2_val = 0

    result = "Ошибка"

    if molecules[0] in acids:
        mol1_type = MolTypes.Acid
        acidResidue_val = mol1[0][1]
    elif mol1_inBrackets in acid_residues:
        mol1_type = MolTypes.Salt
    elif mol1_inBrackets == 'OH':
        mol1_type = MolTypes.Hydroxide
    elif molecules[0] in acid_oxides:
        mol1_type = MolTypes.AcidOxide
    elif len(mol1) > 1 and mol1[1][0] == 'O':
        mol1_type = MolTypes.Oxide

    if molecules[1] in acids:
        mol2_type = MolTypes.Acid
        acidResidue_val = mol2[0][1]
    elif mol2_inBrackets in acid_residues:
        mol2_type = MolTypes.Salt
    elif mol2_inBrackets == 'OH':
        mol2_type = MolTypes.Hydroxide
    elif molecules[1] in acid_oxides:
        mol2_type = MolTypes.AcidOxide
    elif len(mol2) > 1 and mol2[1][0] == 'O':
        mol2_type = MolTypes.Oxide

    elem1_row, elem1_group, elem1_subgoup, elem1_name, _, _, elem1_isMetal, _ = info(mol1[0][0])
    elem2_row, elem2_group, elem2_subgoup, elem2_name, _, _, elem2_isMetal, _ = info(mol2[0][0])

    #валентность внизу
    if mol1_type == MolTypes.Common:
        elem1_val = elem1_group
    if mol2_type == MolTypes.Common: 
        elem2_val = elem2_group

    if mol1_type == MolTypes.Common and mol2_type == MolTypes.Common:
        if  elem1_group > elem2_group:
            elem1_val = 8 - elem1_group
            elem2_val = elem2_group
        elif elem1_group < elem2_group:
            elem2_val = 8 - elem2_group
            elem1_val = elem1_group
        else:
            if elem1_row > elem2_row:
                elem2_val = 8 - elem2_group
                elem1_val = elem1_group
            else:
                elem2_val = elem2_group
                elem1_val = 8 - elem1_group
    elif mol1_type == MolTypes.Oxide:
        elem1_val = mol1[1][1] * 2 // mol1[0][1]
        if mol2_type == MolTypes.AcidOxide:
            if acid_oxides[molecules[1]][1] == '(':
                acidResidue_val = 1
            else:
                acidResidue_val = int(acid_oxides[molecules[1]][1])
    if mol2_type == MolTypes.Oxide:
        elem2_val = mol2[1][1] * 2 // mol2[0][1]
        if mol1_type == MolTypes.AcidOxide:
            if acid_oxides[molecules[0]][1] == '(':
                acidResidue_val = 1
            else:
                acidResidue_val = int(acid_oxides[molecules[0]][1])
    elif mol1_type == MolTypes.Hydroxide:
        elem1_val = mol1[1][1] // mol1[0][1]
        if mol2_type == MolTypes.AcidOxide:
            if acid_oxides[molecules[1]][1] == '(':
                acidResidue_val = 1
            else:
                acidResidue_val = int(acid_oxides[molecules[1]][1])
    elif mol2_type == MolTypes.Hydroxide:
        elem2_val = mol2[1][1] // mol2[0][1]
        if mol1_type == MolTypes.AcidOxide:
            if acid_oxides[molecules[0]][1] == '(':
                acidResidue_val = 1
            else:
                acidResidue_val = int(acid_oxides[molecules[0]][1])

    if elem1_name == "H":
        elem1_val = 1
    elif elem1_name == "O":
        elem1_val = 2

    if elem2_name == "H":
        elem2_val = 1
    elif elem2_name == "O":
        elem2_val = 2
    #валентность наверху

    if mol1_type == MolTypes.Common and elem1_isMetal:
        if mol2_type == MolTypes.Acid:
            result = mol1[0][0] + str(lcm(elem1_val, acidResidue_val) // elem1_val) + "(" + mol2_inBrackets + ")" + str(lcm(elem1_val, acidResidue_val) // acidResidue_val) + " + " + "H2"
    if mol2_type == MolTypes.Common and elem2_isMetal:
        if mol1_type == MolTypes.Acid:
            result = mol2[0][0] + str(lcm(elem2_val, acidResidue_val) // elem2_val) + "(" + mol1_inBrackets + ")" + str(lcm(elem2_val, acidResidue_val) // acidResidue_val) + " + " + "H2"

    if mol1_type == MolTypes.Oxide and elem1_isMetal:
        if mol2_type == MolTypes.Acid:
            result = mol1[0][0] + str(lcm(elem1_val, acidResidue_val) // elem1_val) + "(" + mol2_inBrackets + ")" + str(lcm(elem1_val, acidResidue_val) // acidResidue_val) + " + " + "H2O"
        elif mol2_type == MolTypes.AcidOxide:
            result = mol1[0][0] + str(lcm(elem1_val, acidResidue_val) // elem1_val) + "(" + acid_oxides_2[molecules[1]] + ")" + str(lcm(elem1_val, acidResidue_val) // acidResidue_val)


    if mol2_type == MolTypes.Oxide and elem2_isMetal:
        if mol1_type == MolTypes.Acid:
            result = mol2[0][0] + str(lcm(elem2_val, acidResidue_val) // elem2_val) + "(" + mol1_inBrackets + ")" + str(lcm(elem2_val, acidResidue_val) // acidResidue_val) + " + " + "H2O"
        elif mol1_type == MolTypes.AcidOxide:
            result = mol2[0][0] + str(lcm(elem2_val, acidResidue_val) // elem2_val) + "(" + acid_oxides_2[molecules[0]] + ")" + str(lcm(elem2_val, acidResidue_val) // acidResidue_val)

    if mol1_type == MolTypes.Hydroxide and elem1_isMetal:
        if mol2_type == MolTypes.Acid:
            result = mol1[0][0] + str(lcm(elem1_val, acidResidue_val) // elem1_val) + "(" + mol2_inBrackets + ")" + str(lcm(elem1_val, acidResidue_val) // acidResidue_val) + " + " + "H2O"
        elif mol2_type == MolTypes.AcidOxide and elem2_isMetal == 0:
            result = mol1[0][0] + str(lcm(elem1_val, acidResidue_val) // elem1_val) + "(" + acid_oxides_2[molecules[1]] + ")" + str(lcm(elem1_val, acidResidue_val) // acidResidue_val) + " + H2O"
    if mol2_type == MolTypes.Hydroxide and elem2_isMetal:
        if mol1_type == MolTypes.Acid:
            result = mol2[0][0] + str(lcm(elem2_val, acidResidue_val) // elem2_val) + "(" + mol1_inBrackets + ")" + str(lcm(elem2_val, acidResidue_val) // acidResidue_val) + " + " + "H2O"
        elif mol1_type == MolTypes.AcidOxide and elem1_isMetal == 0:
            result = mol2[0][0] + str(lcm(elem2_val, acidResidue_val) // elem2_val) + "(" + acid_oxides_2[molecules[0]] + ")" + str(lcm(elem2_val, acidResidue_val) // acidResidue_val) + " + H2O"
    if mol1_type == MolTypes.Common and molecules[0] in Alkali_Me:
      if molecules[1] == "H2O":
        if elem1_val > 1:
          result = mol1[0][0] + "(" + "OH" + ")" + str(elem1_val) + " + " + "H2"
        else:
          result = mol1[0][0] + "(" + "OH" + ")" + " + " + "H2"
    if mol1_type == MolTypes.Oxide and mol1[0][0] in Alkali_Me:
      if molecules[1] == "H2O":
          if elem1_val > 1:
            result = mol1[0][0] + "(" + "OH" + ")" + str(elem1_val)
          else:
            result = mol1[0][0] + "(" + "OH" + ")"
    if mol2_type == MolTypes.Common and molecules[1] in Alkali_Me:
      if molecules[0] == "H2O":
          if elem2_val > 1:
            result = mol2[0][0] + "(" + "OH" + ")" + str(elem2_val) + " + " + "H2"
          else:
            result = mol2[0][0] + "(" + "OH" + ")" + " + " + "H2"
    if mol2_type == MolTypes.Oxide and mol2[0][0] in Alkali_Me:
      if molecules[0] == "H2O":
        if elem2_val > 1:
          result = mol2[0][0] + "(" + "OH" + ")" + str(elem2_val)
        else:
          result = mol2[0][0] + "(" + "OH" + ")"
    if mol1_type == MolTypes.AcidOxide:
        if molecules[1] == "H2O":
            result = acid_oxides[molecules[0]]
    if mol2_type == MolTypes.AcidOxide:
        if molecules[0] == "H2O":
            result = acid_oxides[molecules[1]]

    if mol1_type == MolTypes.Common and mol2_type == MolTypes.Common:
        if elem1_group > elem2_group:
            elem1_val = 8 - elem1_group
            elem2_val = elem2_group
        elif elem1_group < elem2_group:
            elem2_val = 8 - elem2_group
            elem1_val = elem1_group
        else:
            if elem1_row > elem2_row:
                elem2_val = 8 - elem2_group
                elem1_val = elem1_group
            else:
                elem2_val = elem2_group
                elem1_val = 8 - elem1_group
        result = mol1[0][0] + str(lcm(elem1_val, elem2_val) // elem1_val) + mol2[0][0] + str(lcm(elem1_val, elem2_val) // elem2_val)

        
    return result

def mol_mass_calc(a):
    counter = 0
    for i in a:
        _, _, _, _, _, mass, _, _ = info(i[0])
        counter += mass * i[1]
    return counter

def React_Calculation(i):
    elem1 = [None, None] # это заглушка
    elem2 = [None, None]
    elems = [None, None]
    elem1_row, elem1_group, elem1_subgroup, elem1_name, _, _, elem1_ismetal, _ = info(elem1[0])
    elem2_row, elem2_group, elem2_subgroup, elem2_name, _, _, elem2_ismetal, _ = info(elem2[0])

    elem1_val = 0
    elem2_val = 0


    if elem1_group > elem2_group:
        elem1_val = 8 - elem1_group
        elem2_val = elem2_group
    elif elem1_group < elem2_group:
        elem2_val = 8 - elem2_group
        elem1_val = elem1_group
    else:
        if elem1_row > elem2_row:
            elem2_val = 8 - elem2_group
            elem1_val = elem1_group
        else:
            elem2_val = elem2_group
            elem1_val = 8 - elem1_group

    if elem1_name == "H":
        elem1_val = 1
    elif elem1_name == "O":
        elem1_val = 2

    if elem2_name == "H":
        elem2_val = 1
    elif elem2_name == "O":
        elem2_val = 2

    elem1_left = 0
    elem1_right = 1
    elem2_left = 2
    elem2_right = 3

    elem1_num = 1
    elem2_num = 1

    if len(elem1) > 2:
        elem1_num = int(elem1[1])
    if len(elem2) > 2:
        elem2_num = int(elem2[1])

    reaction = ""

    if lcm(elem1_val, elem2_val) / elem1_val != 1 and lcm(elem1_val, elem2_val) / elem2_val != 1:
        reaction = elem1[0] + str(lcm(elem1_val, elem2_val) // elem1_val) + elem2[0] + str(lcm(elem1_val, elem2_val) // elem2_val)
    elif lcm(elem1_val, elem2_val) / elem1_val == 1 and lcm(elem1_val, elem2_val) / elem2_val != 1:
        reaction = elem1[0] + elem2[0] + str(lcm(elem1_val, elem2_val) // elem2_val)
    elif lcm(elem1_val, elem2_val) / elem1_val != 1 and lcm(elem1_val, elem2_val) / elem2_val == 1:
        reaction = elem1[0] + str(lcm(elem1_val, elem2_val) // elem1_val) + elem2[0]
    else:
        reaction = elem1[0] + elem2[0]

    elem1_coef = 1
    elem2_coef = 1
    mol_coef = 1

    elem1_index = lcm(elem1_val, elem2_val) // elem1_val
    elem2_index = lcm(elem1_val, elem2_val) // elem2_val

    while elem1_left != elem1_right or elem2_left != elem2_right:
        elem1_right = mol_coef*elem1_index
        elem2_right = mol_coef*elem2_index
        elem1_left = elem1_coef*elem1_num
        elem2_left = elem2_coef*elem2_num
        if elem1_left > elem1_right:
            mol_coef = lcm(elem1_left, elem1_index) // elem1_index
        if elem1_left < elem1_right:
            elem1_coef = lcm(elem1_right, elem1_num) // elem1_num
        if elem2_left > elem2_right:
            mol_coef = lcm(elem2_left, elem2_index) // elem2_index
        if elem2_left < elem2_right:
            elem2_coef = lcm(elem2_right, elem2_num) // elem2_num

    if elem1_coef == 1:
        elem1_coef = ''
    if elem2_coef == 1:
        elem2_coef = ''
    if mol_coef == 1:
        mol_coef = ''

    return str(elem1_coef) + elems[0] + ' + ' + str(elem2_coef) + elems[1] + ' -> ' + str(mol_coef) + reaction

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.CurLineEdit = 0

        uic.loadUi("main_window.ui", self)

        self.pushButton.clicked.connect(self.calculateMolClick)
        self.pushButton_2.clicked.connect(self.calculateReactClick)

        self.lineEdit.installEventFilter(self)
        self.calcmol1.installEventFilter(self)
        self.calcmol2.installEventFilter(self)

        self.pushButton_3.installEventFilter(self)
        self.pushButton_4.installEventFilter(self)
        self.pushButton_5.installEventFilter(self)
        self.pushButton_6.installEventFilter(self)
        self.pushButton_7.installEventFilter(self)
        self.pushButton_8.installEventFilter(self)
        self.pushButton_9.installEventFilter(self)
        self.pushButton_10.installEventFilter(self)
        self.pushButton_11.installEventFilter(self)
        self.pushButton_12.installEventFilter(self)
        self.pushButton_13.installEventFilter(self)
        self.pushButton_14.installEventFilter(self)
        self.pushButton_15.installEventFilter(self)
        self.pushButton_16.installEventFilter(self)
        self.pushButton_17.installEventFilter(self)
        self.pushButton_18.installEventFilter(self)
        self.pushButton_19.installEventFilter(self)
        self.pushButton_20.installEventFilter(self)
        self.pushButton_21.installEventFilter(self)
        self.pushButton_22.installEventFilter(self)
        self.pushButton_23.installEventFilter(self)
        self.pushButton_24.installEventFilter(self)
        self.pushButton_25.installEventFilter(self)
        self.pushButton_26.installEventFilter(self)
        self.pushButton_27.installEventFilter(self)
        self.pushButton_28.installEventFilter(self)
        self.pushButton_29.installEventFilter(self)
        self.pushButton_30.installEventFilter(self)
        self.pushButton_31.installEventFilter(self)
        self.pushButton_32.installEventFilter(self)
        self.pushButton_33.installEventFilter(self)
        self.pushButton_34.installEventFilter(self)
        self.pushButton_35.installEventFilter(self)
        self.pushButton_36.installEventFilter(self)
        self.pushButton_37.installEventFilter(self)
        self.pushButton_38.installEventFilter(self)
        self.pushButton_39.installEventFilter(self)
        self.pushButton_40.installEventFilter(self)
        self.pushButton_41.installEventFilter(self)
        self.pushButton_42.installEventFilter(self)
        self.pushButton_43.installEventFilter(self)
        self.pushButton_44.installEventFilter(self)
        self.pushButton_45.installEventFilter(self)
        self.pushButton_46.installEventFilter(self)
        self.pushButton_47.installEventFilter(self)
        self.pushButton_48.installEventFilter(self)
        self.pushButton_49.installEventFilter(self)
        self.pushButton_50.installEventFilter(self)
        self.pushButton_51.installEventFilter(self)
        self.pushButton_52.installEventFilter(self)
        self.pushButton_53.installEventFilter(self)
        self.pushButton_54.installEventFilter(self)
        self.pushButton_55.installEventFilter(self)
        self.pushButton_56.installEventFilter(self)
        self.pushButton_57.installEventFilter(self)
        self.pushButton_58.installEventFilter(self)
        self.pushButton_59.installEventFilter(self)
        self.pushButton_60.installEventFilter(self)
        self.pushButton_61.installEventFilter(self)
        self.pushButton_62.installEventFilter(self)
        self.pushButton_63.installEventFilter(self)
        self.pushButton_64.installEventFilter(self)
        self.pushButton_65.installEventFilter(self)
        self.pushButton_66.installEventFilter(self)
        self.pushButton_67.installEventFilter(self)
        self.pushButton_68.installEventFilter(self)
        self.pushButton_69.installEventFilter(self)
        self.pushButton_70.installEventFilter(self)
        self.pushButton_71.installEventFilter(self)
        self.pushButton_72.installEventFilter(self)
        self.pushButton_73.installEventFilter(self)
        self.pushButton_74.installEventFilter(self)
        self.pushButton_75.installEventFilter(self)
        self.pushButton_76.installEventFilter(self)
        self.pushButton_77.installEventFilter(self)
        self.pushButton_78.installEventFilter(self)
        self.pushButton_79.installEventFilter(self)
        self.pushButton_80.installEventFilter(self)
        self.pushButton_81.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj.inherits('QAbstractButton') and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                _, _, _, name, full_name, mass, isMetal, pp = info(obj.text())
                self.label_50.setText(name)
                self.label_51.setText(str(pp))
                self.label_52.setText(full_name)
                self.label_53.setText(str(mass))
                ismmm = ''
                if isMetal == True:
                    ismmm = 'Да'
                else:
                    ismmm = 'Нет'
                self.label_54.setText(ismmm)
            elif event.button() == QtCore.Qt.LeftButton:
                if self.CurLineEdit == 1:
                    self.lineEdit.insert(obj.text())
                elif self.CurLineEdit == 2:
                    self.calcmol1.insert(obj.text())
                elif self.CurLineEdit == 3:
                    self.calcmol2.insert(obj.text())
        elif obj == self.lineEdit and event.type() == QtCore.QEvent.FocusIn:
            self.CurLineEdit = 1
        elif obj == self.calcmol1 and event.type() == QtCore.QEvent.FocusIn:
            self.CurLineEdit = 2
        elif obj == self.calcmol2 and event.type() == QtCore.QEvent.FocusIn:
            self.CurLineEdit = 3
        return QtCore.QObject.event(obj, event)

    @QtCore.pyqtSlot()
    def calculateMolClick(self):
        molt = self.lineEdit.text()
        el2d, _ = mol_split(molt)
        self.lineEdit_2.setText(str(mol_mass_calc(el2d)))

    @QtCore.pyqtSlot()
    def calculateReactClick(self):
        moleculsss = [self.calcmol1.text().strip(), self.calcmol2.text().strip()]
        self.lineEdit_3.setText(React_CalculationV2(moleculsss))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())