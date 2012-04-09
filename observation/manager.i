// Copyright (C) 2008-2010, INRIA
// Author(s): Vivien Mallet, Claire Mouton
//
// This file is part of the data assimilation library Verdandi.
//
// Verdandi is free software; you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License as published by the Free
// Software Foundation; either version 2.1 of the License, or (at your option)
// any later version.
//
// Verdandi is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for
// more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with Verdandi. If not, see http://www.gnu.org/licenses/.
//
// For more information, visit the Verdandi web site:
//      http://verdandi.gforge.inria.fr/


%module manager
%{
#include "../../observation/GroundNetworkObservationManager.hxx"
#include "../../observation/EnsembleObservationManager.hxx"

  // TODO: getting rid of the following inclusions.
#include "model/QuadraticModel.hxx"
#include "model/ClampedBar.hxx"
#include "model/PythonModel.hxx"
#include "observation_manager/GridToNetworkObservationManager.hxx"
#include "observation_manager/LinearObservationManager.hxx"
#include "observation_manager/PythonObservationManager.hxx"
#include "method/OptimalInterpolation.hxx"
#include "method/ForwardDriver.hxx"
#include "method/ReducedOrderExtendedKalmanFilter.hxx"
#include "share/Functions_Vector2.hxx"
  %}

%include "std_string.i"
%include "std_vector.i"
using namespace std;

namespace std
{
  %template(vector_string) vector<string>;
}

%import "../../verdandi/python/verdandi.i"

%include "../../verdandi/VerdandiHeader.hxx"
%include "../../verdandi/share/VerdandiBase.hxx"
%include "../../verdandi/share/UsefulFunction.hxx"
%include "../../verdandi/share/Functions_Vector2.hxx"

%include "../../Talos/TalosHeader.hxx"

%include "../../verdandi/include/seldon/vector/Vector2.hxx"
%include "../../verdandi/include/seldon/vector/Vector3.hxx"
%include "../../observation/GroundNetworkObservationManager.hxx"
%include "../../observation/EnsembleObservationManager.hxx"

namespace Seldon
{
  %template(Vector2Int) Vector2<int>;
  %extend Vector2<int>
  {
    %template(HasSameShapeInt) HasSameShape<Vector2<int, MallocAlloc<int>, MallocObject<Vector<int, VectFull, MallocAlloc<int> > > > >;
    %template(HasSameShapeDouble) HasSameShape<Vector2<double, MallocAlloc<double>, MallocObject<Vector<double, VectFull, MallocAlloc<double> > > > >;
    %template(Flatten) Flatten<int, MallocAlloc<int> >;
  }

  %template(Vector2Double) Vector2<double>;
  %extend Vector2<double>
  {
    %template(HasSameShapeDouble) HasSameShape<Vector2<double, MallocAlloc<double>, MallocObject<Vector<double, VectFull, MallocAlloc<double> > > > >;
    %template(HasSameShapeInt) HasSameShape<Vector2<int, MallocAlloc<int>, MallocObject<Vector<int, VectFull, MallocAlloc<int> > > > >;
    %template(Flatten) Flatten<double, MallocAlloc<double> >;
  }

  %template(Vector3Double) Vector3<double>;
  %extend Vector3<double>
  {
    %template(Flatten) Flatten<double, MallocAlloc<double> >;
  }
}

namespace Verdandi
{
  %template(SelectLocationInt) SelectLocation<MallocAlloc<int>, MallocObject<Vector<int, VectFull, MallocAlloc<int> > >, MallocAlloc<int>, MallocObject<Vector<int, VectFull, MallocAlloc<int> > > >;
  %template(SelectLocationDouble) SelectLocation<MallocAlloc<int>, MallocObject<Vector<int, VectFull, MallocAlloc<int> > >, MallocAlloc<int>, MallocObject<Vector<int, VectFull, MallocAlloc<int> > >, double, MallocAlloc<double>, MallocObject<Vector<double, VectFull, MallocAlloc<double> > > >;
}

namespace Polyphemus
{
  %template(GroundNetworkOM) GroundNetworkObservationManager<double>;
  %extend GroundNetworkObservationManager<double>
  {
    %template(ApplyOperator) ApplyOperator<Seldon::Vector<double> >;
  }

  %template(EnsembleOM) EnsembleObservationManager<double>;
}
