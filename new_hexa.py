import streamlit as st
from pentominoes import ALL_PARTS
from polymino import Grid,generate_polyminoes,generate_polymino_positions,unique_grids,solutions_svg
from dlx import DLX
from hexa_rotation_flip import P1,P2,P3,P4,P5,P6,P7,P8

st.title("Hexangeli")
st.write("LEVEL-1")

number = st.selectbox("Select a Date", options=list(range(1, 32)), index=0)
if number==26:
    st.write("OOPS!! NO SOLUTION FOUND")
else:
    date_map={
        1:(0,2),
        2:(0,3),
        3:(0,4),
        4:(0,5),
        5:(0,6),
        6:(0,7),
        7:(1,2),
        8:(1,3),
        9:(1,4),
        10:(1,5),
        11:(1,6),
        12:(1,7),
        13:(2,1),
        14:(2,2),
        15:(2,3),
        16:(2,4),
        17:(2,5),
        18:(2,6),
        19:(2,7),
        20:(3,1),
        21:(3,2),
        22:(3,3),
        23:(3,4),
        24:(3,5),
        25:(3,6),
        26:(4,0),
        27:(4,1),
        28:(4,2),
        29:(4,3),
        30:(4,4),
        31:(4,5)
    }
    date_row_col=date_map[number]

    def sortkey(x):
        x = str(x)
        return (len(x), x)

    COLOURS = dict(I="#f15bb5", F="#9b5de5", L="#00bbf9",
                P="#c7ffff", N="#7aff60", T="#e8fa42",
                U="#fb8f23", V="#f44a4a", W="#AAAAEE",
                X="#BB99DD", Y="#CC88CC", Z="#DD99BB")
    GRID = Grid((5, 8), holes=[(0, 0), (1, 0), (2, 0), (3, 0), (0,1), (1,1), (4,6), (3,7), (4,7),date_row_col])
    print(GRID)
    main_polyminoes=[]

    pieces=[P1,P2,P3,P4,P5,P6,P7,P8]
    shade=['I','F','L','P','N','T','U','V','W','X','Y','Z']

    all_solutions = []  
    j=0

    for SHAPES in pieces:
        polyminoes=[]
        for piece in generate_polyminoes(SHAPES):
            for position in generate_polymino_positions(piece, GRID):
                if position not in polyminoes:
                    polyminoes.append(position)
        polyminoes = [polymino.aslist for polymino in polyminoes]
        polyminoes = [list(reversed(inner_list)) for inner_list in polyminoes]
        for i in polyminoes:
            i.pop()
            i.append(shade[j])
        j+=1
        polyminoes = [list(reversed(inner_list)) for inner_list in polyminoes]
        # print("polyminoes",polyminoes)
        main_polyminoes+=polyminoes

    LABELS = list(set([element for polymino in main_polyminoes for element in polymino]))
    LABELS = sorted(LABELS, key=sortkey)

    # print("Grid\n\n",GRID)
    # print("labels\n\n",LABELS)
    # print("poly\n\n",main_polyminoes)

    COVER = DLX(LABELS, main_polyminoes)
    for i, SOLUTION in enumerate(COVER.generate_solutions()):
        solution_grid = Grid.from_DLX(SOLUTION)
        print(solution_grid)
        all_solutions.append(solution_grid)
        break
    # print(all_solutions)

    solutions_svg([all_solutions[0]], filename='first_solution.svg', columns=7, colour=COLOURS.get)
    svg_content = open("first_solution.svg", "r").read()
    st.write(f"solution for DATE: {number}")
    st.image(svg_content, width=2000)



