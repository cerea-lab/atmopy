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

#define OPS_WITH_EXCEPTION
#define SELDON_DEBUG_LEVEL_2

#include "../../driver/common/observation/GroundNetworkObservationManager.hxx"

  // TODO: getting rid of the following inclusions.
#include "model/QuadraticModel.hxx"
#include "observation_manager/GridToNetworkObservationManager.hxx"
#include "observation_manager/LinearObservationManager.hxx"
#include "method/OptimalInterpolation.hxx"
#include "method/ForwardDriver.hxx"
  %}

%include "std_string.i"
using namespace std;

%import "../../verdandi/python/verdandi.i"

%include "../../verdandi/VerdandiHeader.hxx"
%include "../../verdandi/share/VerdandiBase.hxx"
%include "../../verdandi/share/UsefulFunction.hxx"

%include "../../Talos/TalosHeader.hxx"

%include "../../verdandi/include/seldon/vector/Vector2.hxx"
%include "../../driver/common/observation/GroundNetworkObservationManager.hxx"

namespace Polyphemus
{
  %template(GroundNetworkOM) GroundNetworkObservationManager<double>;
}
