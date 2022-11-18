import ROOT
import math
from ROOT import TLorentzVector, TMath
import numpy 

def makep4(px, py,pz,e):
    p4=TLorentzVector(0.,0.,0.,0.)
    p4.SetPxPyPzE(px, py,pz,e)
    return p4



def ep_arctan(x,y):
    corr=0
    if (x>0 and y>=0) or (x>0 and y<0):
        corr=0
    elif x<0 and y>=0:
        corr=math.pi
    elif x<0 and y<0:
        corr=-math.pi
    if x!=0.:
        return math.atan(y/x)+corr
    else:
        return math.pi/2+corr

def getPtEtaPhiP(px, py, pz, e):
    p_ = DataFrame()
    p_['px'] = px
    p_['py'] = py
    p_['pz'] = pz
    p_['e'] = e
    
    #print type(p_)
    
    pt_=[]
    eta_=[]
    phi_=[]
    p3_=[]
    '''
    #for index,  row in p_.iterrows():
    for row,row1 in zip(p_.px,p_.py):
        print "inside zip loop", row, row1
        #print p_[row[0]]

    
    return [px_,px_,px_,px_]

    '''
    for px_, py_,pz_,e_  in zip(p_.px,p_.py, p_.pz, p_.e):
        '''
        px_ =   row['px']
        py_ =   row['py']
        pz_ =   row['pz']
        e_  =   row['e']
        '''
        ## list comprehension to compute pt 
        pt  = [numpy.sqrt( px_[irow]**2 + py_[irow]**2 ) for irow in range(len(px_))]
        p   = Series([numpy.sqrt( px_[irow]**2 + py_[irow]**2 + pz_[irow]**2) for irow in range(len(px_))])
        eta = [numpy.log((p[irow] + pz_[irow])/(p[irow] - pz_[irow]))/2 for irow in range(len(pz_)) ]
        phi = [numpy.arctan2( py_[irow], px_[irow]) for irow in range(len(px_))]
        
        ## following code make the p4 using list comprehension but its slow. 
        #pt = [makep4(row['px'][irow], row['py'][irow], row['pz'][irow], abs(row['e'][irow])).Pt() for irow in range(len(px_))]
        

        pt_.append(pt)
        eta_.append(eta)
        phi_.append(phi)
        p3_.append(p)
    '''
    p_["pt"]=Series(pt_)
    p_["eta"]=Series(eta_)
    p_["phi"]=Series(phi_)
    p_["p3"]=Series(p3_)
    
    print p_["phi"].head()
    '''
    
    
    return [pt_,eta,phi,p3_]




def getP3(px_, py_, pz_):
    return( numpy.sqrt( px_**2 + py_**2 + pz_**2) )

def getPt(px_, py_):
    return  numpy.sqrt( px_**2 + py_**2)

def getEta(px_, py_, pz_):
    p3_   = getP3(px_, py_, pz_)
    return( numpy.log((p3_ + pz_)/(p3_ - pz_))/2)
    
def getPhi(px_, py_):
    return( numpy.arctan2( py_, px_))


def getPtEtaPhiPFast(px_, py_, pz_, e_):
    '''
    pt_  = numpy.sqrt( px_**2 + py_**2)
    p3_   = numpy.sqrt( px_**2 + py_**2 + pz_**2) 
    eta_ = numpy.log((p3_ + pz_)/(p3_ - pz_))/2
    phi_ = numpy.arctan2( py_, px_)
    '''
    p3_ = getP3(px_, py_, pz_)
    pt_ = getPt(px_, py_)
    eta_ = getEta(px_, py_, pz_)
    phi_=getPhi(px_, py_)
    
    return [pt_,eta_,phi_,p3_]



def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;

def DeltaPhi(phi1,phi2):
   phi = Phi_mpi_pi(phi1-phi2)

   return abs(phi)

def Delta_R(eta1, eta2, phi1,phi2):
    deltaeta = eta1-eta2
    deltaphi = DeltaPhi(phi1,phi2)
    DR = TMath.Sqrt ( deltaeta**2 + deltaphi**2 )
    return DR 

## this function is not needed, just keeping for backward compatibility, 
## p4 already have a function DeltaR 

def DeltaR(p4_1, p4_2):
    eta1 = p4_1.Eta()
    eta2 = p4_2.Eta()
    eta = eta1 - eta2
    eta_2 = eta * eta

    phi1 = p4_1.Phi()
    phi2 = p4_2.Phi()
    phi = Phi_mpi_pi(phi1-phi2)
    phi_2 = phi * phi

    return math.sqrt(eta_2 + phi_2)



def MT(Pt, met, dphi):
    return TMath.Sqrt( 2 * Pt * met * (1.0 - TMath.Cos(dphi)) )


def getMT(Pt, met, phi1, phi2):
    
    dphi = DeltaPhi(phi1, phi2)
    return TMath.Sqrt( 2 * Pt * met * (1.0 - TMath.Cos(dphi)) )

def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;


def InvMass(px1,py1,pz1,pe1,px2,py2,pz2,pe2):
    p1 = TLorentzVector(px1, py1, pz1, pe1)
    p2 = TLorentzVector(px2, py2, pz2, pe2)
    inv_mass = (p1+p2).M()
    return inv_mass


