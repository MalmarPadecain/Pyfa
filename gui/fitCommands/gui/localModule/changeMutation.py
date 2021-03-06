import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localChangeMutation import CalcChangeLocalModuleMutationCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeLocalModuleMutationCommand(wx.Command):

    def __init__(self, fitID, position, mutation, oldMutation=None):
        wx.Command.__init__(self, True, 'Change Local Module Mutation')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.mutation = mutation
        self.oldMutation = oldMutation

    def Do(self):
        cmd = CalcChangeLocalModuleMutationCommand(
            fitID=self.fitID,
            position=self.position,
            mutation=self.mutation,
            oldMutation=self.oldMutation)
        success = self.internalHistory.submit(cmd)
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
