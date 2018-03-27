#initialize global variabls
import expr_classes

def init():

    global n_ErrorSeen     #saved as part of context
    global t_CurToken      #saved as part of context
    global rf_ReadfileList #saved as part of context
    global n_ExitFlag      #saved as part of context

    global n_Debug
    global n_DisplayParsetree
    global v_VarList
    global sz_ShellPrompt
    
    global i_IlkList
    global o_ObjList

    n_Debug = 0    
    n_DisplayParsetree = 0
    n_ErrorSeen = 0
    t_CurToken = 0
    v_VarList = 0
    rf_ReadfileList = 0
    n_ExitFlag = 0
    sz_ShellPrompt = "$ "
    i_IlkList = 0
    o_ObjList = 0
